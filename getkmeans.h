typedef struct {
    float * coordinates_sum;
    int size;

}cluster;
int equal_arr(float** prev, float** curr, int k,int d) ;
float distance(const float * vac1,const float * vac2,int d);
void copy_arr_tow_dim(float **pDouble, float **pDouble1,int K,int d);
void update_centroid(const float* observation, cluster * clusters,int min_index, int d);
void new_centroid(float **curr_cent,  cluster* clusters, int k, int d);
cluster* initialize_cluster(cluster * clusters, int k, int d);
void reset_cluster(cluster * cluster1, int k,  int d);
int Find_min(const float *arr, int k);
int* get_main_c(int K,int N,int d,int MAX_ITER, float ** Observations,float ** curr );

