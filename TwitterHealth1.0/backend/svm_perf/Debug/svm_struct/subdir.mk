################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../svm_struct/svm_struct_classify.o \
../svm_struct/svm_struct_common.o \
../svm_struct/svm_struct_learn.o \
../svm_struct/svm_struct_main.o 

C_SRCS += \
../svm_struct/svm_struct_classify.c \
../svm_struct/svm_struct_common.c \
../svm_struct/svm_struct_learn.c \
../svm_struct/svm_struct_main.c 

OBJS += \
./svm_struct/svm_struct_classify.o \
./svm_struct/svm_struct_common.o \
./svm_struct/svm_struct_learn.o \
./svm_struct/svm_struct_main.o 

C_DEPS += \
./svm_struct/svm_struct_classify.d \
./svm_struct/svm_struct_common.d \
./svm_struct/svm_struct_learn.d \
./svm_struct/svm_struct_main.d 


# Each subdirectory must supply rules for building sources it contributes
svm_struct/%.o: ../svm_struct/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


