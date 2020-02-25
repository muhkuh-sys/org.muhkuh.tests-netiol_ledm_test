#ifndef __VECTORS_H__
#define __VECTORS_H__


typedef void (*RISCV_VECT_T)(void);



typedef struct RISCV_VECTOR_TABLE_STRUCT
{
	RISCV_VECT_T apfnInterrupts[32];
	RISCV_VECT_T pfnReset;
	RISCV_VECT_T pfnIllegalInstruction;
	RISCV_VECT_T pfnECallHandler;
} RISCV_VECTOR_TABLE_T;


#endif  /* __VECTORS_H__ */
