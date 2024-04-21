/*
*	In His Exalted Name
*	Matrix Addition - Sequential Code
*	Ahmad Siavashi, Email: siavashi@aut.ac.ir
*	15/04/2018
*/

// Let it be.
#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <omp.h>
#include <math.h>

using namespace std;

typedef struct {
	int *A, *B, *C;
	int n, m;
} DataSet;

void fillDataSet(DataSet *dataSet);
void printDataSet(DataSet dataSet);
void closeDataSet(DataSet dataSet);
void add(DataSet *dataSet);
void add_1d(DataSet *dataSet);
void add_2d(DataSet *dataSet);

#define NUM_THREADS 8

// 0 -> serial, 1 -> 1D multi-threading, 2 -> 2D multi-threading
#define SUM_MODE 2

#define PRINT_DS 0

int chunk_size;

int main(int argc, char *argv[]) {
	DataSet dataSet;
	if (argc < 3) {
		printf("[-] Invalid No. of arguments.\n");
		printf("[-] Try -> <n> <m> \n");
		printf(">>> ");
		scanf("%d %d", &dataSet.n, &dataSet.m);
	}
	else {
		dataSet.n = atoi(argv[1]);
		dataSet.m = atoi(argv[2]);
	}
	
    if(SUM_MODE > 0)
		printf("%d X %d with %d threads, ", dataSet.n, dataSet.m, NUM_THREADS);
	else
		printf("%d X %d with no multi-threading, ", dataSet.n, dataSet.m);
	
	fillDataSet(&dataSet);

    printf("size=%0.2fMB\n", (double)(sizeof(int) * dataSet.n * dataSet.m)/(1024.0*1024.0));
    
	if(SUM_MODE == 2){
		chunk_size = (int)ceil(sqrt(max(dataSet.n, dataSet.m)));
		printf("chunk_size=%d\n", chunk_size);
	}

    double starttime = omp_get_wtime();

	if(SUM_MODE == 0)
		add(&dataSet);
	else if(SUM_MODE == 1)
		add_1d(&dataSet);
	else if(SUM_MODE == 2)
		add_2d(&dataSet);
	else
		printf("Invalid SUM_MODE: %d", SUM_MODE);

    double elapsedtime = omp_get_wtime() - starttime;
    printf("Time Elapsed for A+B: %fSecs\n", elapsedtime);

	if(PRINT_DS)
		printDataSet(dataSet);

	closeDataSet(dataSet);

	// commented because of runtime error
	// system("PAUSE");
	getchar();

	return EXIT_SUCCESS;
}

void fillDataSet(DataSet *dataSet) {
	int i, j;

	dataSet->A = (int *)malloc(sizeof(int) * dataSet->n * dataSet->m);
	dataSet->B = (int *)malloc(sizeof(int) * dataSet->n * dataSet->m);
	dataSet->C = (int *)malloc(sizeof(int) * dataSet->n * dataSet->m);

	srand(time(NULL));

	for (i = 0; i < dataSet->n; i++) {
		for (j = 0; j < dataSet->m; j++) {
			dataSet->A[i*dataSet->m + j] = rand() % 100;
			dataSet->B[i*dataSet->m + j] = rand() % 100;
		}
	}
}

void printDataSet(DataSet dataSet) {
	int i, j;

	printf("[-] Matrix A\n");
	for (i = 0; i < dataSet.n; i++) {
		for (j = 0; j < dataSet.m; j++) {
			printf("%-4d", dataSet.A[i*dataSet.m + j]);
		}
		putchar('\n');
	}

	printf("[-] Matrix B\n");
	for (i = 0; i < dataSet.n; i++) {
		for (j = 0; j < dataSet.m; j++) {
			printf("%-4d", dataSet.B[i*dataSet.m + j]);
		}
		putchar('\n');
	}

	printf("[-] Matrix C\n");
	for (i = 0; i < dataSet.n; i++) {
		for (j = 0; j < dataSet.m; j++) {
			printf("%-8d", dataSet.C[i*dataSet.m + j]);
		}
		putchar('\n');
	}
}

void closeDataSet(DataSet dataSet) {
	free(dataSet.A);
	free(dataSet.B);
	free(dataSet.C);
}

void add(DataSet *dataSet) {
	printf("Using simple add function...\n");

	int i, j;

	for (i = 0; i < dataSet->n; i++) {
		for (j = 0; j < dataSet->m; j++) {
			dataSet->C[i * dataSet->m + j] = dataSet->A[i * dataSet->m + j] + dataSet->B[i * dataSet->m + j];
		}
	}
}

void add_1d(DataSet *dataSet) {
	printf("Using add_1d function...\n");
	int i, j;

    #pragma omp parallel for num_threads(NUM_THREADS) private(j) firstprivate(dataSet)
	for (i = 0; i < dataSet->n; i++) {
		for (j = 0; j < dataSet->m; j++) {
			dataSet->C[i * dataSet->m + j] = dataSet->A[i * dataSet->m + j] + dataSet->B[i * dataSet->m + j];
		}
	}
}

void add_2d(DataSet *dataSet) {
	printf("Using add_2d function...\n");

	int n_chunks = (int)ceil((double)dataSet->n / chunk_size),
		 m_chunks = (int)ceil((double)dataSet->m / chunk_size);
	printf("n_chunks=%d, m_chunks=%d\n", n_chunks, m_chunks);

	#pragma omp parallel for num_threads(NUM_THREADS) collapse(2) firstprivate(dataSet)
	for(int i = 0; i < n_chunks; i++) {
		for(int j = 0; j < m_chunks; j++) {
			for(int k = i*chunk_size; k < min((i+1)*chunk_size, dataSet->n); k++) {
				for(int l = j*chunk_size; l < min((j+1)*chunk_size, dataSet->m); l++) {
					dataSet->C[k * dataSet->m + l] = dataSet->A[k * dataSet->m + l] + dataSet->B[k * dataSet->m + l];
				}
			}

		}
	}
}
