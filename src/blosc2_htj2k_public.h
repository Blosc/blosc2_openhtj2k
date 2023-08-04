#ifndef PUBLIC_WRAPPER_H
#define PUBLIC_WRAPPER_H

#ifdef __cplusplus
extern "C" {
#else
#include <stdbool.h>
#endif

#if defined(_MSC_VER)
#define BLOSC2_OPENHTJ2K_EXPORT __declspec(dllexport)
#elif (defined(__GNUC__) && __GNUC__ >= 4) || defined(__clang__)
#if defined(_WIN32) || defined(__CYGWIN__) || defined(__MINGW32__)
  #define BLOSC2_OPENHTJ2K_EXPORT __attribute__((dllexport))
#else
  #define BLOSC2_OPENHTJ2K_EXPORT __attribute__((visibility("default")))
#endif  /* defined(_WIN32) || defined(__CYGWIN__) */
#else
#error Cannot determine how to define BLOSC2_OPENHTJ2K_EXPORT for this compiler.
#endif

#define BLOSC_CODEC_OPENHTJ2K 244

BLOSC2_OPENHTJ2K_EXPORT int blosc2_openhtj2k_encoder(
  				const uint8_t* input,
  				int32_t input_len,
  				uint8_t* output,
  				int32_t output_len,
  				uint8_t meta,
  				blosc2_cparams* cparams,
  				const void* chunk
				);

BLOSC2_OPENHTJ2K_EXPORT int blosc2_openhtj2k_decoder(
  				const uint8_t *input,
  				int32_t input_len,
 				uint8_t *output,
  				int32_t output_len,
  				uint8_t meta,
  				blosc2_dparams *dparams,
  				const void* chunk
				);

BLOSC2_OPENHTJ2K_EXPORT codec_info info = {
    .encoder=(char *)"blosc2_openhtj2k_encoder",
    .decoder=(char *)"blosc2_openhtj2k_decoder"
};

/* Helper function to register the codec */
void blosc2_openhtj2k_register(blosc2_codec *codec) {
  codec->compcode = BLOSC_CODEC_OPENHTJ2K;
  codec->version = 1;
  codec->complib = 1;
  codec->compname = (char*)"openhtj2k";
  codec->encoder = NULL;
  codec->decoder = NULL;
  blosc2_register_codec(codec);
}


#ifdef __cplusplus
}
#endif

#endif
