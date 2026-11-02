#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <algorithm>
#include <ctime>
#include <random>

std::vector<int> hamming_encode(const std::vector<int>& bit_arr) {
    if (bit_arr.size() < 120) {
        return bit_arr;
    }

    std::vector<int> encoded_arr = encode(bit_arr, 7);
    encoded_arr.insert(encoded_arr.begin(), std::reduce(encoded_arr.begin(), encoded_arr.end(), 0, std::bit_xor<int>()));
    return encoded_arr;
}

std::vector<int> encode(const std::vector<int>& bit_arr, int max_pow) {
    std::vector<int> encoded_bit_arr = bit_arr;

    for (int i = 0; i < max_pow; ++i) {
        encoded_bit_arr.insert(encoded_bit_arr.begin() + (1 << i) - 1, 0);
    }

    int step = 2;
    for (int i : {1, 2, 4}) {
        int parity_bit_index = i - 1;
        std::vector<int> parity_check_bit_list;

        while (parity_bit_index < encoded_bit_arr.size()) {
            parity_check_bit_list.insert(parity_check_bit_list.end(), encoded_bit_arr.begin() + parity_bit_index,
                encoded_bit_arr.begin() + std::min(parity_bit_index + step / 2, static_cast<int>(encoded_bit_arr.size())));

            parity_bit_index += step;
        }

        int parity = std::reduce(parity_check_bit_list.begin(), parity_check_bit_list.end(), 0, std::bit_xor<int>());
        encoded_bit_arr[parity_bit_index] = parity;
        step *= 2;
    }

    return encoded_bit_arr;
}

std::vector<int> errors_generator(const std::vector<int>& bit_arr, int errors) {
    std::vector<int> bits_with_errors = bit_arr;

    if (errors == 1) {
        int error_i = std::rand() % bit_arr.size();
        bits_with_errors[error_i] = !bits_with_errors[error_i];
    }

    if (errors >= 2) {
        std::vector<int> mas;
        for (int i = 0; i < errors; ++i) {
            int error_i = std::rand() % bit_arr.size();
            if (std::find(mas.begin(), mas.end(), error_i) == mas.end()) {
                mas.push_back(error_i);
                bits_with_errors[error_i] = !bits_with_errors[error_i];
            }
            else {
                --i;
            }
        }
    }

    return bits_with_errors;
}

std::vector<int> hamming_decode(const std::vector<int>& bit_arr) {
    if (bit_arr.size() < 128) {
        return bit_arr;
    }

    std::vector<int> hamming_coded_arr(bit_arr.begin() + 1, bit_arr.end());
    int parity_bit = bit_arr[0];
    auto [decoded_arr, error] = decode(hamming_coded_arr, 7);

    int parity = std::reduce(hamming_coded_arr.begin(), hamming_coded_arr.end(), 0, std::bit_xor<int>());
    if (error != -1 && parity == parity_bit) {
        std::cout << "\n\n      More than 1 error\n\n";
        return std::vector<int>();
    }

    return decoded_arr;
}

std::pair<std::vector<int>, int> decode(const std::vector<int>& bit_arr, int max_pow) {
    int step = 2;
    int error_bit_index = -1;

    for (int i : {1, 2, 4}) {
        int parity_bit_index = i - 1;
        std::vector<int> parity_check_bit_list;

        while (parity_bit_index < bit_arr.size()) {
            parity_check_bit_list.insert(parity_check_bit_list.end(), bit_arr.begin() + parity_bit_index,
                bit_arr.begin() + std::min(parity_bit_index + step / 2, static_cast<int>(bit_arr.size())));

            parity_bit_index += step;
        }

        parity_check_bit_list[0] = 0;
        int parity = std::reduce(parity_check_bit_list.begin(), parity_check_bit_list.end(), 0, std::bit_xor<int>());

        if (parity != bit_arr[parity_bit_index]) {
            if (error_bit_index == -1) {
                error_bit_index = parity_bit_index;
            }
            else {
                error_bit_index += parity_bit_index + 1;
            }
        }

        step *= 2;
    }

    if (error_bit_index != -1) {
        std::cout << "The error was found on the position: " << error_bit_index << std::endl;
        bit_arr[error_bit_index] = !bit_arr[error_bit_index];
    }
    else {
        std::cout << "There is no error." << std::endl;
    }

    for (int i = max_pow; i > 0; --i) {
        bit_arr.erase(bit_arr.begin() + (1 << (i - 1)) - 1);
    }

    return std::make_pair(bit_arr, error_bit_index);
}

void encode_file(const std::string& file_name, int errors) {
    std::ifstream input_file(file_name, std::ios::binary);
    std::ofstream output_file(file_name + "d.txt", std::ios::binary);

    while (true) {
        std::vector<int> bytes_f;
        char raw_bytes[15];
        input_file.read(raw_bytes, sizeof(raw_bytes));
        if (input_file.gcount() == 0) {
            break;
        }

        bytes_f.insert(bytes_f.end(), raw_bytes, raw_bytes + input_file.gcount());
        std::vector<int> bytes_t = hamming_encode(bytes_f);
        std::vector<int> bytes_er = errors_generator(bytes_t, errors);
        for (int bit : bytes_er) {
            output_file.put(bit);
        }
    }
}

void decode_file(const std::string& file_name, const std::string& out_file) {
    std::ifstream input_file(file_name + "d.txt", std::ios::binary);
    std::ofstream output_file(out_file, std::ios::binary);

    while (true) {
        std::vector<int> bytes_from_file;
        char raw_bytes[16];
        input_file.read(raw_bytes, sizeof(raw_bytes));
        if (input_file.gcount() == 0) {
            break;
        }

        bytes_from_file.insert(bytes_from_file.end(), raw_bytes, raw_bytes + input_file.gcount());
        std::vector<int> bytes_to_file = hamming_decode(bytes_from_file);
        if (!bytes_to_file.empty()) {
            for (int bit : bytes_to_file) {
                output_file.put(bit);
            }
        }
        else {
            break;
        }
    }
}

int main() {
    std::string in_f = "text.txt";
    std::string out_f = "out.txt";

    while (true) {
        std::cout << "\n1. Encode\n2. Decode\n3. Encode and decode\n4. Out\n";
        std::cout << "Choose a func: ";
        std::string op;
        std::cin >> op;

        if (op == "1") {
            int mis_num;
            std::cout << "How many mistakes: ";
            std::cin >> mis_num;
            encode_file(in_f, mis_num);
        }
        else if (op == "2") {
            decode_file(in_f, out_f);
        }
        else if (op == "3") {
            int mis_num;
            std::cout << "How many mistakes: ";
            std::cin >> mis_num;
            encode_file(in_f, mis_num);
            decode_file(in_f, out_f);
        }
        else if (op == "4") {
            break;
        }
    }

    return 0;
}
