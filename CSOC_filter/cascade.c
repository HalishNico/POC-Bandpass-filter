
#include <stdio.h>  
#include <stdlib.h>
#include <string.h> 
#include <math.h>

# define M_PI           3.14159265358979323846

struct filterStruct{
    struct filterStruct *CSOS;  
    float input;
    float output;
    float delay_1;
    float delay_2;
    float coefs[4];
};

struct filterStruct *filter = NULL;

void loop_coefs(){
    struct filterStruct *next= filter;
    while(next != NULL){
        printf("Iteration   0 \n");
        for(int i=0;i<4;i++){
            printf("coefficient %i %f  \n", i,next->coefs[i]);
        }
        printf("Iteration   1\n");
        next=next->CSOS;
        printf("Iteration   2\n");
    }
    printf("Iteration   3 \n");
    return;
};

// High pass:

// Middle frequencies bandpass:   1.0,0,-1.0,0, -1.553312629199899,0.9216,0,0,

// Low pass: -1.0,0,1.0,0, 0.5933126291998989,0.9216,-1.3543299167663192,0.5776, 0.5933126291998992,0.9216,-1.3543299167663192,0.5776,
// Gain = 0.0047

int output(float _input){
    struct filterStruct *next= filter;
    int block_count=0;
    _input=_input*0.467;
    while(next != NULL){
        //  filter input
        next->input=_input+next->delay_1*next->coefs[2] + next->delay_2*next->coefs[3];
        //  filter output 
        next->output=next->input + next->delay_1*next->coefs[0] + next->delay_2*next->coefs[1];
        //  renew the values of the delay blocks
        //printf("block %i , delay 1  %f \n", block_count, next->delay_1);
        //printf("block %i , delay 2  %f \n", block_count, next->delay_2);
        next->delay_2=next->delay_1;
        next->delay_1=next->input;
        _input= next->output;
        if(next->CSOS == NULL){
            break;
        }
        next=next->CSOS;
        block_count++;
    }
    for(int i=0, n=(int)next->output;i<n;i++){
        printf("#");
    }
    printf("%f", next->output);
    printf("\n");
};


int main(int argc, char** argv){
    struct filterStruct *next = (struct filterStruct*)malloc(sizeof(struct filterStruct));
    filter=next;
    if(argc <2){
        printf("Need an input of poles/zeroes \n");
        return 1;
    }
    char *token;
    for(int i=1;i<argc;i++){
        next->CSOS = (struct filterStruct*)malloc(sizeof(struct filterStruct));
        next=next->CSOS;
        int iLen = strlen(argv[i]);
        char *sInput = (char *)malloc((iLen+1) * sizeof(char));
        strcpy(sInput, argv[i]);
        char s[2] = ",";
        token = strtok(sInput, s);
        int iteration=0;
        while(token != NULL){
            next->coefs[iteration] = -atof(token);
            token = strtok(NULL ,s);
            iteration++;
        }
    }
    filter=filter->CSOS;
    float pulse_time=0;
    float input;
    while(pulse_time<256){
        input = 10.0*cosf(3*M_PI*pulse_time/256.0) + 10.0*cosf(4.0*M_PI*pulse_time/5.0);
        pulse_time++;
        output(input);
    }
    return 0;
};