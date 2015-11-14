
#include <stdio.h>
#include <stdlib.h>

typedef struct {
	int x;
	int pd;
} point;

void process_bucket (point * bucket, int size_t bucket_size) {

}

int main (int argc, char * argv) {

	FILE * fp = fopen("clean_csv.csv", "r");


	size_t bucket_size = 1000;
	int i = 0;
	point bucket[bucket_size];

	char *  line;
	size_t  len = 0;
	ssize_t bytes_read = 0;

	while ((bytes_read = getline(&line, &len, fp) != -1)) {
		char * x_str  = (char *)strtok(line, ",");
		char * pd_str = (char *)strtok(NULL, ",");

		point p;

		p.x  = atoi(x_str);
		p.pd = atoi(pd_str);

		if (i != 0 && i % bucket_size == 0) {
			bucket[i] = p;
		} else {
			i++;
		}
	}

	return 0;
}