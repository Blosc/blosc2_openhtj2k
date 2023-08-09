#include <string>
#include <vector>

#include "dec_utils.hpp"
#include "encoder.hpp"

#include "utils.h"


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


int blosc2_openhtj2k_read_image(image_t *image, const char *filename)
{
    // Parse image
    std::vector<std::string> filenames = {filename};
    open_htj2k::image img(filenames);

    // Load general information
    image->num_components = img.get_num_components();
    image->width = img.get_width();
    image->height = img.get_height();
    image->max_bpp = img.get_max_bpp();

    // Load component information
    image->buffer_len = 0;
    for (uint16_t c = 0; c < image->num_components; ++c) {
        uint32_t width = img.get_component_width(c);
        uint32_t height = img.get_component_height(c);
        uint32_t size = width * height * sizeof(int32_t);
        uint8_t ssiz = img.get_Ssiz_value(c);
        image->components[c].width = width;
        image->components[c].height = height;
        image->components[c].ssiz = ssiz;
        image->components[c].depth = (ssiz & 0x7F) + 1;
        image->components[c].sign = ssiz >> 7;
        image->buffer_len += size;
    }

    // Copy data to contiguous array
    image->buffer = (uint8_t*)malloc(image->buffer_len);
    uint8_t *dest = image->buffer;
    for (uint16_t c = 0; c < image->num_components; ++c) {
        uint32_t width = image->components[c].width;
        uint32_t height = image->components[c].height;
        uint32_t size = width * height * sizeof(int32_t);
        memcpy(dest, img.get_buf(c), size);
        dest += size;
    }

    return 0;
}

void blosc2_openhtj2k_free_image(image_t *image)
{
    free(image->buffer);
    image->buffer = NULL;
}

int blosc2_openhtj2k_write_ppm(
    uint8_t *input,
    int64_t input_len,
    image_t *image,
    char *filename
)
{
    std::vector<int32_t *> buf;
    std::vector<uint32_t> img_width;
    std::vector<uint32_t> img_height;
    std::vector<uint8_t> img_depth;
    std::vector<bool> img_signed;

    uint8_t *dest = input;
    for (uint16_t c = 0; c < image->num_components; c++) {
        uint32_t width = image->components[c].width;
        uint32_t height = image->components[c].height;
        uint32_t size = width * height * sizeof(int32_t);
        img_width.push_back(width);
        img_height.push_back(height);
        img_depth.push_back(image->components[c].depth);
        img_signed.push_back(image->components[c].sign);
        buf.push_back((int32_t*)dest);
        dest += size;
    }

    char *ext = strrchr(filename, '.');
    write_ppm(filename, ext, buf, img_width, img_height, img_depth, img_signed);

    return 0;
}
