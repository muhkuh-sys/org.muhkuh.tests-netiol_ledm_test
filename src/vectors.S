	.section .vector_table, "ax"

	.global tVectorTable
	.extern start

/*------------------------------------*/

tVectorTable:
	jal     x0, 0        /* IRQ  0 */
	jal     x0, 0        /* IRQ  1 */
	jal     x0, 0        /* IRQ  2 */
	jal     x0, 0        /* IRQ  3 */
	jal     x0, 0        /* IRQ  4 */
	jal     x0, 0        /* IRQ  5 */
	jal     x0, 0        /* IRQ  6 */
	jal     x0, 0        /* IRQ  7 */
	jal     x0, 0        /* IRQ  8 */
	jal     x0, 0        /* IRQ  9 */
	jal     x0, 0        /* IRQ 10 */
	jal     x0, 0        /* IRQ 11 */
	jal     x0, 0        /* IRQ 12 */
	jal     x0, 0        /* IRQ 13 */
	jal     x0, 0        /* IRQ 14 */
	jal     x0, 0        /* IRQ 15 */
	jal     x0, 0        /* IRQ 16 */
	jal     x0, 0        /* IRQ 17 */
	jal     x0, 0        /* IRQ 18 */
	jal     x0, 0        /* IRQ 19 */
	jal     x0, 0        /* IRQ 20 */
	jal     x0, 0        /* IRQ 21 */
	jal     x0, 0        /* IRQ 22 */
	jal     x0, 0        /* IRQ 23 */
	jal     x0, 0        /* IRQ 24 */
	jal     x0, 0        /* IRQ 25 */
	jal     x0, 0        /* IRQ 26 */
	jal     x0, 0        /* IRQ 27 */
	jal     x0, 0        /* IRQ 28 */
	jal     x0, 0        /* IRQ 29 */
	jal     x0, 0        /* IRQ 30 */
	jal     x0, 0        /* IRQ 31 */

	jal     x0, start    /* Reset */
	jal     x0, 0        /* Illegal instruction */
	jal     x0, 0        /* ECALL handler */
