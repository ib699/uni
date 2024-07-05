#include <iostream>
#include <cmath>
#include <omp.h>
#define NUM_THREADS 8
#define NUM_STEPS 100000

int main()
{
    static double step_len = 10.0 / (double)NUM_STEPS;
    double result = 0.0;

    // Use a single variable for the sum and make it private to each thread to avoid false sharing
    // Reduction clause is used to safely accumulate the results from each thread
#pragma omp parallel num_threads(NUM_THREADS) reduction(+:result)
    {
        double x;
        double sum = 0.0; // Local variable for each thread to accumulate its partial sum
        int thread_id = omp_get_thread_num();
        int num_threads = omp_get_num_threads(); // Correctly moved inside the parallel region

        for (int i = thread_id; i < NUM_STEPS; i += num_threads)
        {
            x = (i + 0.5) * step_len - 5.0;
            sum += exp(-(x * x));
        }
        // Accumulate the partial sum into the result variable using the reduction clause
        result += sum * step_len;
    }

    std::cout << "Result: " << result << std::endl;
    return 0;
}