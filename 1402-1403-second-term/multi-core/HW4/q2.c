#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define max(x, y) (((x) > (y)) ? (x) : (y))

int lcs(char *a, char *b, size_t a_len, size_t b_len)
{
    // Set up dynamic programming memoization matrix
    int(*dp)[a_len + 1][b_len + 1] = malloc(sizeof(int[a_len + 1][b_len + 1]));
    size_t y_len = a_len + 1;
    size_t x_len = b_len + 1;

    // Zero out first row and first column
    for(int i = 0; i < y_len; i++)
    {
        (*dp)[i][0] = 0;
    }

    for(int i = 0; i < x_len; i++)
    {
        (*dp)[0][i] = 0;
    }

    // Parallelize the LCS computation using OpenMP tasks
    #pragma omp parallel
    {
        #pragma omp single
        {
            for (int i = 1; i < y_len; i += 128)
            {
                for (int j = 1; j < x_len; j += 128)
                {
                    #pragma omp task
                    {
                        int end_i = i + 128 < y_len ? i + 128 : y_len;
                        int end_j = j + 128 < x_len ? j + 128 : x_len;

                        for (int k = i; k < end_i; k++)
                        {
                            for (int l = j; l < end_j; l++)
                            {
                                if (a[k-1] == b[l-1])
                                {
                                    (*dp)[k][l] = (*dp)[k - 1][l - 1] + 1;
                                }
                                else
                                {
                                    (*dp)[k][l] = max((*dp)[k - 1][l], (*dp)[k][l - 1]);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    int retval = (*dp)[a_len][b_len];
    free(dp);
    return retval;
}

int main()
{
    size_t string_size = 1 << 15;

    char *str1 = malloc(string_size + 1);
    char *str2 = malloc(string_size + 1);
    srand(500); // Fix rand seed to have the same string for every run

    for(int i = 0; i < string_size; i++)
    {
        str1[i] = (rand() % 26) + 97;
        str2[i] = (rand() % 26) + 97;
    }

    // Null terminate strings
    str1[string_size] = '\0';
    str2[string_size] = '\0';

    printf("%d\n", lcs(str1, str2, string_size, string_size));

    return 0;
}

