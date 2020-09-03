#ifndef OP_H
#define OP_H

struct {
    void (*exec)(char *, struct mos6500 *);
    char num_cycles;
    char num_bytes;
} op;

#endif /* end of include guard: OP_H */