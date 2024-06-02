/*
*				In His Exalted Name
*	Title:	Prefix Sum Sequential Code
*	Author: Ahmad Siavashi, Email: siavashi@aut.ac.ir
*	Date:	29/04/2018
*/

// Let it be.
#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef long long int ll;

void fill_array(ll *a, size_t n);
void prefix_sum(ll *a, size_t n);
void print_array(int *a, size_t n);

int main(int argc, char *argv[]) {
	// Input N
	size_t n = 0;
	printf("[-] Please enter N: ");
	scanf("%uld\n", &n);

	// Allocate memory for array
	ll * a = (ll *)malloc(n * sizeof(ll));
	// Fill array with numbers 1..n
	fill_array(a, n);
	// Print array
	// print_array(a, n);

	// Compute prefix sum
	clock_t tStart = clock();
	prefix_sum(a, n);
	printf("Elapsed time in sec %lf\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);

	// Print array
	// print_array(a, n);

	if(a[n-1] != (n*(n+1)/2))
		printf("oops! result is wrong!\n");

	// Free allocated memory
	free(a);
	return EXIT_SUCCESS;
}

void prefix_sum(ll *a, size_t n) {
	int i;
	for (i = 1; i < n; ++i) {
		a[i] = a[i] + a[i - 1];
	}
}

void print_array(ll *a, size_t n) {
	int i;
	printf("[-] array: ");
	for (i = 0; i < n; ++i) {
		printf("%lld, ", a[i]);
	}
	printf("\b\b \n");
}

void fill_array(ll *a, size_t n) {
	int i;
	for (i = 0; i < n; ++i) {
		a[i] = i + 1;
	}
}
