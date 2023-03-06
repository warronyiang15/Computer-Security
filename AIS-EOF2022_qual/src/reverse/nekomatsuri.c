#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char possible_key[100] = {
    0xa6, 0x68, 0x19, 0xb0,
    0x94, 0x8f, 0x5f, 0xa1,
    0x8b, 0x20, 0x0d, 0x54,
    0x3b, 0xf7, 0x57, 0x3c,
    0x00
};

unsigned char input[1000];

unsigned char _a1[1000] = {
    0xa6, 0x68, 0x19, 0xb0,
    0x94, 0x8f, 0x5f, 0xa1,
    0x8b, 0x20, 0x0d, 0x54,
    0x3b, 0xf7, 0x57, 0x3c,
    0x00,
};

unsigned char _a3[1000] = {
    0x8f, 0xe6, 0xc7, 0x84,
    0xa6, 0x68, 0x19, 0xb0,
    0x94, 0x8f, 0x5f, 0xa1,
    0x8b, 0x20, 0x0d, 0x54,
    0x3b, 0xf7, 0x57, 0x3c,
    0x00,
};

unsigned char ModuleName[100] = {
    0xD8, 0x47, 0x8e, 0x00,
    0x37, 0x9b, 0x6f, 0x95,
    0xa6, 0x85, 0x12, 0x54, 
    0x85, 0x00,
};

unsigned char enc_flag[100] = {
    0x1c, 0xf5, 0x9e, 0x13, 0x7f, 0x21, 0xc5, 0x0d,
    0x15, 0x3a, 0xe6, 0xf8, 0xa7, 0x9e, 0x9f, 0xec,
    0x56, 0x6d, 0xf8, 0x2c, 0xf0, 0x80, 0xa6, 0x96,
    0x04, 0x8c, 0xb9, 0x6f, 0x8b, 0xcc, 0x74, 0x43,
    0x3a, 0xa1, 0x07, 0x10, 0x55, 0x47, 0xd2, 0x96,
    0x36, 0x9d, 0x8e, 0x6b, 0x84, 0x89, 0x7e, 0xc4,
    0x63, 0xe6, 0x61, 0x9b, 0x7a, 0xd7, 0xad, 0x32,
    0xad, 0x82, 0x4a, 0x67, 0x04, 0x7e, 0x32, 0xca,
    0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
};

unsigned char Win_Exec_arr[100] = {
    0x93, 0x38, 0xc3, 0x5a, 0x59, 0xe3, 0x68, 0x76
};

void swap(char* a,char *b){
    unsigned char tmep = *a;
    *a = *b;
    *b = tmep;
}


void sus(unsigned char* a1,signed int a2, unsigned char* a3, int a4, char a5){
    char v5[268];
    char v6;
    unsigned char v7;
    char v8;
    unsigned char v9;
    int k;
    int j;
    int i;
    unsigned char v13;
    
    v6 = v8 = 0;
    v7 = v9 = v13 = 0;
    i = j = k =0;
    
    // Built up the v5
    for(i = 0;i <= 255; ++i)
        v5[i] = i;
    v13 = 0;
    for(j = 0;j <= 255; ++j)
    {
        v13 += v5[j] + a3[j % a4];
        swap(&v5[j], &v5[v13]);
        //v5[j] ^= v5[v13];
        //v5[v13] ^= v5[j];
        //v5[j] ^= v5[v13];
    }
    
    // need reverse
    v13 = 0;
    for(k = 0;k < a2; ++k){
        v9 = k + 1;
        v8 = v5[(k + 1)];
        v13 += v8;
        v5[(k + 1)] ^= v5[v13];
        v5[v13] ^= v5[v9];
        v5[v9] ^= v5[v13];
        v7 = v5[v9] + v8;
        v6 = v5[v7];
        if( a5 >= 0 )
            a1[k] = v6 ^ (a1[k] + a5);
        else
            a1[k] = (v6 ^ a1[k]) + a5; 
    }
    return;
}

int main(void){
    unsigned char flag[100];
    unsigned char argv1[100] = {
        'C', 'h', '1', 'y', '0', 'd', '4', 'm', '0', 'm', '0'
    };
    unsigned char mmmm[100] = {
        'W', 'i', 'n', '_', 'E', 'x', 'e', 'c'
    };
    const char* a = "Ch1y0d4m0m0";
    unsigned char test[100];
    for(int i = 0;i < 16;i++){
        test[i] = possible_key[i];
    }
    
    sus(possible_key, 16, _a3, 4, 3);
    sus(ModuleName, 13, possible_key, 16, 143);
    printf("%s\n", ModuleName);
    sus(ModuleName, 13, possible_key, 16, -143);
    sus(possible_key, 16, _a3, 4, -3);
    for(int i = 0;i < 16;i++){
        if(test[i] != possible_key[i]){
            printf("wrong\n");
        }
    }
    
    sus(possible_key, 16, _a3, 4, 3);
    sus(Win_Exec_arr, 8, possible_key, 16, 192);
    printf("%s\n", Win_Exec_arr);
    
    sus(possible_key, 16, _a3, 4, -3);
    
    sus(possible_key, 16, Win_Exec_arr, 7, 253);
    sus(enc_flag, 65, possible_key, 16, 30);
    for(int i = 0;i <= 64;i++){
        printf("%x ", enc_flag[i]);
        flag[i] = i ^ argv1[i % 11] ^ enc_flag[i];
    }
    printf("%s\n", flag);
    return 0;
}