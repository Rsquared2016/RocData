flush;
x = [0.1, 0.8, 0.3]; %cpt of p
%% train data
train_num = 1500;

train_file = ['hmm_train_' num2str(train_num) 'data.txt'];
train_true_labels_file = ['hmm_train_' num2str(train_num) 'true_labels.txt'];
train = [x(1)>rand(1,train_num/3) x(2)>rand(1,train_num/3) ...
    x(3)>rand(1,train_num/3)];
truth_perm = randperm(train_num);
train=train(truth_perm);

fid_train = fopen(train_file, 'w');
if(fid_train == -1) error('Could not open file %s for writing', train_file); end

fid_train_truth = fopen(train_true_labels_file, 'w');
if(fid_train_truth == -1) error('Could not open file %s for writing', train_file_truth); end
% truth = [find(truth_perm <= train_num/3) ...
%     find((truth_perm > train_num/3) & (truth_perm <= train_num/3*2)) ...
%     find(truth_perm > train_num/3*2)];
t = [zeros(1,train_num/3) ones(1,train_num/3) ...
    2*ones(1,train_num/3)];

for i = 1:train_num
    fprintf(fid_train, '%d\n', train(i));
    fprintf(fid_train_truth, '%d\n', t(truth_perm(i)));
end
fclose(fid_train);
fclose(fid_train_truth);
%% test data
test_num = 9000;

test_file = ['hmm_test_' num2str(test_num) 'data.txt'];
test_true_labels_file = ['hmm_test_'  num2str(test_num) 'true_labels.txt'];
test = [x(1)>rand(1,test_num/3) x(2)>rand(1,test_num/3) ...
    x(3)>rand(1,test_num/3)];
truth_perm = randperm(test_num);
test=test(truth_perm);

fid_test = fopen(test_file, 'w');
if(fid_test == -1) error('Could not open file %s for writing', test_file); end

fid_test_truth = fopen(test_true_labels_file, 'w');
if(fid_test_truth == -1) error('Could not open file %s for writing', test_file_truth); end
% truth = [find(truth_perm <= test_num/3) ...
%     find((truth_perm > test_num/3) & (truth_perm <= test_num/3*2)) ...
%     find(truth_perm > test_num/3*2)];

t = [zeros(1,test_num/3) ones(1,test_num/3) ...
    2*ones(1,test_num/3)];

for i = 1:test_num
    fprintf(fid_test, '%d\n', test(i));
    fprintf(fid_test_truth, '%d\n', t(truth_perm(i)));
end
fclose(fid_test);
fclose(fid_test_truth);