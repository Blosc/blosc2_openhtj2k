#ifndef BLOSC2_OPENHTJ2K_UTILS_H
#define BLOSC2_OPENHTJ2K_UTILS_H

#include "blosc2_htj2k.h"

#ifdef __cplusplus
extern "C" {
#endif

int blosc2_openhtj2k_read_image(image_t *image, const char *filename);
void blosc2_openhtj2k_free_image(image_t *image);
int blosc2_openhtj2k_write_ppm(uint8_t *input, int64_t input_len, image_t *image, char *filename);

#ifdef __cplusplus
}
#endif

#endif
