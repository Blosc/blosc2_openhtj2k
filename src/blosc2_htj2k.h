#ifndef WRAPPER_H
#define WRAPPER_H

#ifdef __cplusplus
extern "C" {
#else
#include <stdbool.h>
#endif

#include "blosc2.h"
#include "b2nd.h"
#include "blosc2/codecs-registry.h"


typedef struct {
  uint16_t blkwidth;
  uint16_t blkheight;
  bool is_max_precincts;
  bool use_SOP;
  bool use_EPH;
  uint8_t progression_order;
  uint16_t number_of_layers;
  uint8_t use_color_trafo;
  uint8_t dwt_levels;
  uint8_t codeblock_style;
  uint8_t transformation;
} blosc2_openhtj2k_cod_params;

typedef struct {
  uint8_t number_of_guardbits;
  bool is_derived;
  double base_step;
} blosc2_openhtj2k_qcd_params;

typedef struct {
  uint8_t qfactor;
  bool isJPH;
  uint8_t color_space;
  uint32_t XOsiz;
  uint32_t YOsiz;
  uint32_t XTsiz;
  uint32_t YTsiz;
  uint32_t XTOsiz;
  uint32_t YTOsiz;
  blosc2_openhtj2k_cod_params *cod;
  blosc2_openhtj2k_qcd_params *qcd;
  uint32_t nthreads;
} blosc2_openhtj2k_params;

/* Extra functions */
typedef struct {
  uint32_t width;
  uint32_t height;
  uint8_t depth; // default 8
  bool sign;     // default 0
  uint8_t ssiz;  // component's bit depth and sign (combines the 2 above)
} component_t;

typedef struct {
  uint8_t *buffer;
  int32_t buffer_len;
  uint32_t width;
  uint32_t height;
  uint8_t max_bpp;
  uint16_t num_components;
  component_t components[3];
} image_t;


int set_params_defaults(
  uint8_t qfactor,
  bool isJPH,
  uint8_t color_space,
  uint32_t nthreads,
  uint16_t cod_blkwidth,
  uint16_t cod_blkheight,
  bool cod_is_max_precincts,
  bool cod_use_SOP,
  bool cod_use_EPH,
  uint8_t cod_progression_order,
  uint16_t cod_number_of_layers,
  uint8_t cod_use_color_trafo,
  uint8_t cod_dwt_levels,
  uint8_t cod_codeblock_style,
  uint8_t cod_transformation,
  uint8_t qcd_number_of_guardbits,
  bool qcd_is_derived,
  double qcd_base_step
);

#ifdef __cplusplus
}
#endif

#endif
