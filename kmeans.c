
#define PY_SSIZE_T_CLEAN  /* For all # variants of unit formats (s#, y#, etc.) use Py_ssize_t rather than int. */
#include <Python.h>       /* MUSTֲ includeֲ <Python.h>, this implies inclusion of the following standard headers:
                             <stdio.h>, <string.h>, <errno.h>, <limits.h>, <assert.h> and <stdlib.h> (if available). */
#include "getkmeans.h"


/*
 * API functions
 */
static PyObject* get_main_api(PyObject *self, PyObject *args)
{
    PyObject *_list, *_list2;
    PyObject *item, *item2;
    PyObject *clusters_index;
    int k,n,d,max;
    int i,j;
    float ** observation;
    float ** centroids;
    int * output;


    if(!PyArg_ParseTuple(args, "iiiiOO", &k,&n,&d,&max,&_list,&_list2)) {
        return NULL;
    }

     observation = (float **) malloc(n* sizeof(float *));/*array of centroids*/
     centroids = (float **) malloc(k * sizeof(float *));
         if (observation == NULL || centroids==NULL) {
    	PyErr_SetString(PyExc_NameError,"memory allocation failed");
        return NULL;
    }


    /* Is it a list? */
    if (!PyList_Check(_list)||!PyList_Check(_list2))
        return NULL;

      /*Go over each item of the list and reduce it */

      for (i = 0; i < k; i++) {
        item = PyList_GetItem(_list2, i);
        Py_INCREF(item);

        PyObject *item_inside;
        float* centroid = malloc(d * sizeof(double));
       if (centroid==NULL){
            PyErr_SetString(PyExc_NameError ,"memory allocation failed");
            return NULL;
        }
         for (j = 0; j < d; j++) {
            item_inside = PyList_GetItem(item, j);
             Py_INCREF(item_inside);

            centroid[j] = PyFloat_AsDouble(item_inside);
            Py_DECREF(item_inside);

        }
        Py_DECREF(item);

        centroids[i] = centroid;
    }

    for (i = 0; i < n; i++) {
        item2 = PyList_GetItem(_list, i);
         Py_INCREF(item2);

        PyObject *item_inside;
        float* x_i = malloc(d * sizeof(float));
        if (x_i==NULL){
            PyErr_SetString(PyExc_NameError ,"memory allocation failed");
            return NULL;
        }
            for (j = 0; j < d; j++) {
            item_inside = PyList_GetItem(item2, j);
            Py_INCREF(item_inside);
            x_i[j] = PyFloat_AsDouble(item_inside);
            Py_DECREF(item_inside);

        }
         Py_DECREF(item2);

        observation[i] = x_i;

    }

    output = (int*)malloc(n * sizeof(int));
    if (output==NULL){
            PyErr_SetString(PyExc_NameError ,"memory allocation failed");
            return NULL;
        }

    output = get_main_c(k,n,d,max, observation, centroids);


    clusters_index = PyList_New(n);
    for (i=0;i<n;i++){
         PyList_SetItem(clusters_index, i, PyFloat_FromDouble(output[i]));
    }

/* This builds the answer ("d" = Convert a C double to a Python floating point number) back into a python object */
    return Py_BuildValue("O", clusters_index); /*  Py_BuildValue(...) returns a PyObject*  */
   /*return Py_BuildValue("i", get_main_c(k,n,d,max, observation, centroids));*/
}

/*
 * This array tells Python what methods this module has.
 * We will use it in the next structure
 */

static PyMethodDef capiMethods[] = {
    {"get_main",                   /* the Python method name that will be used */
      (PyCFunction)  get_main_api, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parameters
accepted for this function */
      PyDoc_STR("A geometric series up to n. sum_up_to_n(z^n)")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all                                 of the functions for the module have been defined. */
};

/* This initiates the module using the above definitions. */
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    capiMethods /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    PyObject *n;
    n = PyModule_Create(&moduledef);
    if (!n) {
    return NULL;
    }
    return n;
}

















