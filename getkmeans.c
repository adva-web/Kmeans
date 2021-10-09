#include "getkmeans.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


cluster* initialize_cluster(cluster * clusters, int k, int d){
    int i,j;
    for (j=0;j<k; j++){
        cluster c;
        c.size=0;
        c.coordinates_sum = (float *) malloc(d * sizeof(float));
   if (c.coordinates_sum==NULL){
            printf("memory allocation failed");
            exit(1);
        }
   for (i=0;i<d; i++) {
            c.coordinates_sum[i] = 0;
        }
        clusters[j] = c;
    }
    return clusters;
}

int Find_min(const float *arr, int k) {
    int r, index;
    float min;
    index = 0;
    min = arr[0];
    for(r=0;r<k;r++){
        if (arr[r] < min){
            index = r;
            min = arr[r];
        }
    }
    return index;
}
/*compares two arrays*/
int equal_arr(float** prev, float** curr, int k,int d) { /*compares between 2 arrays of centroids*/
    int p,r;
    double epsilon;
    epsilon = 0.0001;
    for ( p = 0; p < k; p++) {
        for (r = 0; r < d; r++) {
            if ((prev[p][r]-curr[p][r]) > epsilon) {
                return 0;
            }
        }
    }
    return 1;
}

/*determines which cluster should the observation should go into*/
float distance(const float * vac1,const float * vac2,int d){/*sum 2 vector;*/
    float sum;
    int j;
    sum=0;
    for (j=0;j<d;j++){
        sum+=(vac1[j]-vac2[j])*(vac1[j]-vac2[j]);
    }
    return sum;

}
/*updates coordinates_sum with a new observation*/
void update_centroid(const float* observation, cluster * clusters,int min_index, int d){
    int q;
        for (q=0;q<d;q++){
            clusters[min_index].coordinates_sum[q]+=observation[q];
        }

    }
/*calculates the new arrays of centroids and put it in curr*/
void new_centroid(float **curr_cent,  cluster* clusters, int k, int d) {
        int i,j;
        for(i=0; i<k; i++){
            for (j=0;j<d;j++){
                curr_cent[i][j] = clusters[i].coordinates_sum[j]/ (float)clusters[i].size;
            }
        }
}
/*copies array to anther array in 2 dim*/
void copy_arr_tow_dim(float **pDouble, float **pDouble1,int K,int d) {
    int l,m;
    for(l=0;l<K;l++){
        for(m=0;m<d;m++){
            pDouble[l][m]=pDouble1[l][m];
        }
    }


}
/*reset the clusters*/
void reset_cluster(cluster * cluster1, int k,  int d) {
    int x,y;
    for(y=0;y<k;y++) {
        cluster1[y].size=0;
        for (x = 0; x < d; x++) {
            cluster1[y].coordinates_sum[x] = 0;
        }
    }
}


int* get_main_c(int K,int N,int d,int MAX_ITER, float ** Observations,float ** curr ){
        int counter;
        int e,m;
        int r;
        int p;
        int x,b;
        cluster *clusters;
        float ** prev;
        int * clusters_index;

     prev = (float **) malloc(K * sizeof(float *));/*array of centriod*/
     clusters = (cluster *) malloc(K * sizeof(cluster));/*size of K=3*/
    if (clusters==NULL){
       printf("memory allocation failed");
       exit(1);
      }

    for (e = 0; e < K; e++) {
            prev[e] = (float *) malloc(d * sizeof(float));
              if (prev[e]==NULL){
              printf("memory allocation failed");
              exit(1);
             }
            for(m=0;m<d;m++){
                prev[e][m]=0;
            }
        }
    clusters = initialize_cluster(clusters,K,d);
    counter=0;
    float *distan;
    distan = (float *)malloc(K* sizeof(float));
      if (distan==NULL){
       printf("memory allocation failed");
       exit(1);
    }
    while(counter<MAX_ITER && !equal_arr(curr,prev,K,d)){
        copy_arr_tow_dim(prev,curr,K,d);/*copies curr to prev*/
        reset_cluster(clusters,K,d);
        for(x=0;x<N;x++) {
            int min_index;
            for (b = 0; b < K; b++) {
                distan[b] = distance(Observations[x], prev[b], d);
            }
            min_index = Find_min(distan, K);
            update_centroid(Observations[x],clusters,min_index,d);
            clusters[min_index].size++;
        }
        new_centroid(curr,clusters,K,d);
        counter++;
    }
    clusters_index = (int *) malloc(N* sizeof(int));
    if (clusters_index==NULL){
       printf("memory allocation failed");
       exit(1);
    }
   for(x=0 ; x<N ;x++ ){

        for (b = 0; b < K; b++) {
                distan[b] = distance(Observations[x], curr[b], d);
            }
            clusters_index[x] =  Find_min(distan, K);
   }
/*frees the memory */
    free(distan);
    distan=NULL;
    for (p=0 ; p < K; p++) {
            free(prev[p]);
            free(curr[p]);
            curr[p] = NULL;
            prev[p] = NULL;
        }

        free(prev);
        prev=NULL;
        free(curr);
        curr=NULL;
    for (p = 0; p <N; p++) {
        free(Observations[p]);
        Observations[p] = NULL;
    }
    free(Observations);
    Observations = NULL;
    for (r=0;r<K; r++){
            free(clusters[r].coordinates_sum);
            clusters[r].coordinates_sum = NULL;
        }
        free(clusters);
        clusters=NULL;
        return clusters_index;
    }
