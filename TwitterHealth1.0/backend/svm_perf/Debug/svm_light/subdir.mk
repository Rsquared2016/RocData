################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../svm_light/svm_common.o \
../svm_light/svm_hideo.o \
../svm_light/svm_learn.o \
../svm_light/svm_learn_main.o 

C_SRCS += \
../svm_light/svm_classify.c \
../svm_light/svm_common.c \
../svm_light/svm_hideo.c \
../svm_light/svm_learn.c \
../svm_light/svm_learn_main.c \
../svm_light/svm_loqo.c 

OBJS += \
./svm_light/svm_classify.o \
./svm_light/svm_common.o \
./svm_light/svm_hideo.o \
./svm_light/svm_learn.o \
./svm_light/svm_learn_main.o \
./svm_light/svm_loqo.o 

C_DEPS += \
./svm_light/svm_classify.d \
./svm_light/svm_common.d \
./svm_light/svm_hideo.d \
./svm_light/svm_learn.d \
./svm_light/svm_learn_main.d \
./svm_light/svm_loqo.d 


# Each subdirectory must supply rules for building sources it contributes
svm_light/%.o: ../svm_light/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


