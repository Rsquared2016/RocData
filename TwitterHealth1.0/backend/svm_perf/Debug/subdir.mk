################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../svm_struct_api.o \
../svm_struct_learn_custom.o 

C_SRCS += \
../svm_struct_api.c \
../svm_struct_learn_custom.c 

OBJS += \
./svm_struct_api.o \
./svm_struct_learn_custom.o 

C_DEPS += \
./svm_struct_api.d \
./svm_struct_learn_custom.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


