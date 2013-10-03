/***********************************************************************/
/*                                                                     */
/*   svm_struct_classify.c                                             */
/*                                                                     */
/*   Classification module of SVM-struct.                              */
/*                                                                     */
/*   Author: Thorsten Joachims                                         */
/*   Date: 03.07.04                                                    */
/*                                                                     */
/*   Copyright (c) 2004  Thorsten Joachims - All rights reserved       */
/*                                                                     */
/*   This software is available for non-commercial use only. It must   */
/*   not be modified and distributed without prior permission of the   */
/*   author. The author is not responsible for implications from the   */
/*   use of this software.                                             */
/*                                                                     */
/************************************************************************/

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <assert.h>
#include <unistd.h>

#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include "../svm_light/svm_common.h"
#ifdef __cplusplus
}
#endif
#include "../svm_struct_api.h"
#include "svm_struct_common.h"


char testfile[200];
char modelfile[200];
char predictionsfile[200];

void read_input_parameters(int, char **, char *, char *, char *, 
			   STRUCT_LEARN_PARM *, long*, long *, long *);
void print_help(void);

int createSocket(long socket_id)
{      
	char address[128];
    register int s;
    socklen_t len;
    struct sockaddr_un saun;

    // use this unique socket address
    assert(sprintf(address, "svm_socket_%ld", socket_id) > 0);
    printf("This instance's socket address: %s\n", address);
    
    /*
     * Get a socket to work with.  This socket will
     * be in the UNIX domain, and will be a
     * stream socket.
     */
    if ((s = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        perror("server: socket");
        exit(1);
    }

    /*
     * Create the address we will be binding to.
     */
    saun.sun_family = AF_UNIX;
    strcpy(saun.sun_path, address);
    printf("This instance's socket address: %s\n", saun.sun_path);
    
    /*
     * Try to bind the address to the socket.  We
     * unlink the name first so that the bind won't
     * fail.
     *
     * The third argument indicates the "length" of
     * the structure, not just the length of the
     * socket name.
     */
    unlink(address);
    len = sizeof(struct sockaddr_un);
    
    if (bind(s, (struct sockaddr *) &saun, len) < 0) {
        perror("server: bind");
        exit(1);
    }

    /*
     * Listen on the socket.
     */
    if (listen(s, 5) < 0) {
        perror("server: listen");
        exit(1);
    }
    return s;
}

void readSocket(FILE *fp) {
    char c;
    while ((c = fgetc(fp)) != EOF) {        
        putchar(c);
        if (c == '\n')
            break;
        }
}

void writeSocket(int ns, double score) {
    char buffer [32];
    assert(sprintf(buffer, "%.8f\n", score) > 0);
    send(ns, buffer, strlen(buffer), 0);
}


int main (int argc, char* argv[])
{
  long i;
  STRUCTMODEL model;
  STRUCT_LEARN_PARM sparm;
  SAMPLE testsample;
  LABEL y;

  // Socket variables
  FILE *fp;
  struct sockaddr_un fsaun;
  socklen_t fromlen;
  int sock, ns;
  long socket_id;

  svm_struct_classify_api_init(argc,argv);
  read_input_parameters(argc,argv,testfile,modelfile,predictionsfile,&sparm,
			&verbosity,&struct_verbosity,&socket_id);

  if(struct_verbosity>=1) {
    printf("Reading model..."); fflush(stdout);
  }
  model=read_struct_model(modelfile,&sparm);
  if(struct_verbosity>=1) {
    fprintf(stdout, "done.\n");
  }

  if(model.svm_model->kernel_parm.kernel_type == LINEAR) { /* linear kernel */
    /* compute weight vector */
      add_weight_vector_to_linear_model(model.svm_model);
    model.w=model.svm_model->lin_weights;
  }

  printf("Listening and ready to classify.\n");
  
  // Read, classify, and return classification for examples 
  while (1) {
		// Init Socket
		sock = createSocket(socket_id);
		//printf("Listening and ready to classify.\n");
		/*
		 * Accept connections.  When we accept one, ns
		 * will be connected to the client.  fsaun will
		 * contain the address of the client.
		 */
		if ((ns = accept(sock, (struct sockaddr *) &fsaun, &fromlen)) < 0) {
			perror("server: accept");
			exit(1);
		}

		// We'll use stdio for reading the socket.
		fp = fdopen(ns, "r");

		if (struct_verbosity>=1) {
			printf("Reading test examples...");
			fflush(stdout);
		}
		//readSocket(fp);
		testsample=read_struct_examples(fp, &sparm);
		if (struct_verbosity>=1) {
			printf("done.\n");
			fflush(stdout);
		}

		if (struct_verbosity>=1) {
			printf("Classifying test examples...");
			fflush(stdout);
		}
		//t1=get_runtime();
		y=classify_struct_example(testsample.examples[0].x, &model, &sparm);
		if (struct_verbosity>=1) {
			printf("done.\n");
			fflush(stdout);
		}
		//runtime+=(get_runtime()-t1);
		// y contains all classification scores
		//write_label(predfl,y);
		for (i=0; i<y.totdoc; i++) {
			//printf("c: %f\n", y.class[i]);
			writeSocket(ns, y.class[i]);
		}
		free_label(y);
		//print_struct_testing_stats(testsample,&model,&sparm,&teststats);
		free_struct_sample(testsample);
		close(sock);
                if (fp > 0) {
                    fclose(fp);
                }
                if (ns > 0){
                    close(ns);
                }
	}
	free_struct_model(model);
	svm_struct_classify_api_exit();
	return (0);
}

void read_input_parameters(int argc,char *argv[],char *testfile,
			   char *modelfile,char *predictionsfile,
			   STRUCT_LEARN_PARM *struct_parm,
			   long *verbosity,long *struct_verbosity,long *socket_id)
{
  long i;
  
  /* set default */
  strcpy (modelfile, "svm_model");
  strcpy (predictionsfile, "svm_predictions"); 
  (*verbosity)=0;/*verbosity for svm_light*/
  (*struct_verbosity)=1; /*verbosity for struct learning portion*/
  struct_parm->custom_argc=0;

  for(i=1;(i<argc) && ((argv[i])[0] == '-');i++) {
    switch ((argv[i])[1]) 
      { 
      case 'h': print_help(); exit(0);
      case '?': print_help(); exit(0);
      case '-': strcpy(struct_parm->custom_argv[struct_parm->custom_argc++],argv[i]);i++; strcpy(struct_parm->custom_argv[struct_parm->custom_argc++],argv[i]);break; 
      case 'v': i++; (*struct_verbosity)=atol(argv[i]); break;
      case 'y': i++; (*verbosity)=atol(argv[i]); break;
      case 's': i++; (*socket_id)=atol(argv[i]); break;
      default: printf("\nUnrecognized option %s!\n\n",argv[i]);
	       print_help();
	       exit(0);
      }
  }
  if((i+1)>=argc) {
    printf("\nNot enough input parameters!\n\n");
    print_help();
    exit(0);
  }
  strcpy (testfile, argv[i]);
  strcpy (modelfile, argv[i+1]);
  if((i+2)<argc) {
    strcpy (predictionsfile, argv[i+2]);
  }

  parse_struct_parameters_classify(struct_parm);
}

void print_help(void)
{
  printf("\nSVM-struct classification module: %s, %s, %s\n",INST_NAME,INST_VERSION,INST_VERSION_DATE);
  printf("   includes SVM-struct %s for learning complex outputs, %s\n",STRUCT_VERSION,STRUCT_VERSION_DATE);
  printf("   includes SVM-light %s quadratic optimizer, %s\n",VERSION,VERSION_DATE);
  copyright_notice();
  printf("   usage: svm_struct_classify [options] example_file model_file output_file\n\n");
  printf("options: -h         -> this help\n");
  printf("         -v [0..3]  -> verbosity level (default 2)\n\n");

  print_struct_help_classify();
}




