# `sytx+func` bucket — worked examples

Combined: code structure differs AND behaviour differs.

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0x9a4c90a8b908fc09`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.133)</th>
<th align="left">v2-sys (max=0.133)</th>
<th align="left">v2.1-sys (max=0.937)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(query.size(2) / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
):
    is_alias = (
        query._storage().data_ptr()
        == key._storage().data_ptr()
        == value._storage().data_ptr()
    )

    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    chunk_grad_outputs: bool = (
        (not grad_kv_needs_init)
        and M == N
        and query.size(3) == value.size(3)
        and is_alias
    )

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )

    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


>>>>>>> b
@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
```

</td>
<td valign="top">

```python
@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
        aten._scaled_dot_product_efficient_attention,
        aten._scaled_dot_product_efficient_attention_backward,
        aten.scatter_reduce.two,
        aten.scatter_reduce.two_out,
    ]
)
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python
@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
        aten._scaled_dot_product_efficient_attention,
        aten._scaled_dot_product_efficient_attention_backward,
        aten.scatter_reduce.two,
        aten.scatter_reduce.two_out,
    ]
)
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python
@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
        aten._scaled_dot_product_efficient_attention,
        aten._scaled_dot_product_efficient_attention_backward,
        aten.scatter_reduce.two,
        aten.scatter_reduce.two_out,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(query.size(2) / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
):
    is_alias = (
        query._storage().data_ptr()
        == key._storage().data_ptr()
        == value._storage().data_ptr()
    )

    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    chunk_grad_outputs: bool = (
        (not grad_kv_needs_init)
        and M == N
        and query.size(3) == value.size(3)
        and is_alias
    )

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )

    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
@out_wrapper()
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python

@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(M / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
    chunk_grad_outputs=False,
):
    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )
    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.133**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.133**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.937**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.930)</th>
<th align="left">v2-sys (max=0.073)</th>
<th align="left">v2.1-sys (max=0.097)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(query.size(2) / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
):
    is_alias = (
        query._storage().data_ptr()
        == key._storage().data_ptr()
        == value._storage().data_ptr()
    )

    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    chunk_grad_outputs: bool = (
        (not grad_kv_needs_init)
        and M == N
        and query.size(3) == value.size(3)
        and is_alias
    )

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )

    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


>>>>>>> b
@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
```

</td>
<td valign="top">

```python
src = src_or_value if isinstance(src_or_value, torch.Tensor) else None
    scatter_meta_impl(self, dim, index, src, reduce)
    return self


@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(query.size(2) / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
):
    is_alias = (
        query._storage().data_ptr()
        == key._storage().data_ptr()
        == value._storage().data_ptr()
    )

    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    chunk_grad_outputs: bool = (
        (not grad_kv_needs_init)
        and M == N
        and query.size(3) == value.size(3)
        and is_alias
    )

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )

    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
@out_wrapper()
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python
@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
@out_wrapper()
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python
src = src_or_value if isinstance(src_or_value, torch.Tensor) else None
    scatter_meta_impl(self, dim, index, src, reduce)
    return self


@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
@out_wrapper()
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
```

</td>
<td valign="top">

```python

@register_meta(
    [
        aten._scaled_dot_product_flash_attention,
    ]
)
def meta__scaled_dot_product_flash(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    return_softmax: bool = False,
    is_causal: bool = False,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)
    head_dim = query.size(3)

    max_seqlen_batch_k = key.size(2)

    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    Nnz_q = batch_size * max_seqlen_batch_q

    output = torch.empty(
        (Nnz_q, num_heads, head_dim), dtype=query.dtype, device=query.device
    )
    ouput = output.view(batch_size, max_seqlen_batch_q, num_heads, head_dim).transpose(
        1, 2
    )
    max_seqlen_q = math.ceil(max_seqlen_batch_q / 16) * 16
    logsumexp = torch.empty(
        (batch_size, num_heads, max_seqlen_q),
        dtype=torch.float,
        device=query.device,
    )
    is_sm80 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (8, 0)
    is_sm75 = torch.cuda.is_available() and torch.cuda.get_device_capability() >= (7, 5)
    head_size_rounded = 64 if head_dim <= 64 else 128
    blocksize_c = (
        128
        if (head_size_rounded == 128 and (dropout_p != 0.0 or not is_sm80))
        or (is_sm75 and head_size_rounded == 64 and dropout_p != 0.0)
        else 256
    )
    max_seqlen_k = math.ceil(max_seqlen_batch_k / blocksize_c) * blocksize_c
    if max_seqlen_k <= 128:
        max_seqlen_k = 128
    elif max_seqlen_k <= 256:
        max_seqlen_k = 256

    softmax = torch.empty(
        (batch_size, num_heads, max_seqlen_q, max_seqlen_k),
        dtype=query.dtype,
        device=query.device,
    )
    return ouput, logsumexp, softmax


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention,
    ]
)
def meta__scaled_dot_product_efficient(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    compute_log_sumexp: bool,
    is_causal: bool = False,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    K = query.size(-1)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_dim = math.ceil(M / 32) * 32 if compute_log_sumexp else 0
    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    return res, logsum_exp


@register_meta(
    [
        aten._scaled_dot_product_efficient_attention_backward,
    ]
)
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    is_causal: bool = False,
    chunk_grad_outputs=False,
):
    grad_out = grad_out.transpose(1, 2)
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    nH = query.size(2)
    K = query.size(3)

    grad_kv_needs_init = is_causal and N > M

    if chunk_grad_outputs:
        chunk = torch.empty((B, M, 3, nH, K), dtype=query.dtype, device=query.device)
        grad_q = chunk.select(2, 0)
        grad_k = chunk.select(2, 1)
        grad_v = chunk.select(2, 2)
    else:
        grad_q = torch.empty(query.shape, dtype=query.dtype, device=query.device)
        grad_k = (
            torch.zeros(key.shape, dtype=key.dtype, device=key.device)
            if grad_kv_needs_init
            else torch.empty(key.shape, dtype=key.dtype, device=key.device)
        )
        grad_v = (
            torch.zeros(value.shape, dtype=value.dtype, device=value.device)
            if grad_kv_needs_init
            else torch.empty(value.shape, dtype=value.dtype, device=value.device)
        )
    return grad_q.transpose(1, 2), grad_k.transpose(1, 2), grad_v.transpose(1, 2)


```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.930**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.073**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.097**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x5213872d22f71b0f`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.840)</th>
<th align="left">v2-sys (max=0.765)</th>
<th align="left">v2.1-sys (max=0.765)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a


def test_main():
    test_support.run_unittest(distutils.tests.test_suite())
    test_support.reap_children()
=======
import test.test_support


def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
>>>>>>> b

```

</td>
<td valign="top">

```python
from test import test_support
import distutils.tests

def test_main():
    test_support.run_unittest(distutils.tests.test_suite())
    test_support.reap_children()

if __name__ == "__main__":
    test_main()
```

</td>
<td valign="top">

```python
def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
```

</td>
<td valign="top">

```python
def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
```

</td>
<td valign="top">

```python
import distutils.tests


def test_main():
    test_support.run_unittest(distutils.tests.test_suite())
    test_support.reap_children()
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 1.5× over-gen &nbsp;·&nbsp; max=**0.840**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.765**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.765**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.757)</th>
<th align="left">v2-sys (max=0.844)</th>
<th align="left">v2.1-sys (max=0.876)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a


def test_main():
    test_support.run_unittest(distutils.tests.test_suite())
    test_support.reap_children()
=======
import test.test_support


def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
>>>>>>> b

```

</td>
<td valign="top">

```python
import test.test_support


def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
    test.test_support.reap_children()


if __name__ == "__main__":
    test_main()
```

</td>
<td valign="top">

```python
import test.test_support


def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
    test.test_support.reap_children()
```

</td>
<td valign="top">

```python
def test_main():
    test.test_support.run_unittest(distutils.tests.test_suite())
    test.test_support.reap_children()
```

</td>
<td valign="top">

```python
import distutils.tests


def test_main():
    test_support.run_unittest(distutils.tests.test_suite())
    test_support.reap_children()
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.757**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.844**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.876**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0x2e0e97e7426557cc`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


>>>>>>> b
# copy_ fails when trying to write to tensors with memory overlap,
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
        raise TypeError("Input must be a torch.Tensor")
    return t.dim() - t.sizes().count(1)
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
        raise TypeError("Input must be a torch.Tensor")
    return t.dim() - t.dim_where(lambda x: x == 1).size(0)
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
        raise TypeError("Input must be a torch.Tensor")
    return t.dim() - 1
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 902.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 921.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 885.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


>>>>>>> b
# copy_ fails when trying to write to tensors with memory overlap,
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
```

</td>
<td valign="top">

```python
@dataclasses.dataclass
class BoxedBool:
    value: bool

    def __bool__(self):
        return self.value

    @staticmethod
    def disable(obj):
        if isinstance(obj, BoxedBool):
            obj.value = False
            return obj
        return False


@dataclasses.dataclass
class BoxedDeviceIndex:
    value: Optional[int]

    def set(self, device_idx):
        assert device_idx is None or isinstance(device_idx, int)
        self.value = device_idx


# copy_ fails when trying to write to tensors with memory overlap,
# for expanded dimensions (a dimension which used to have size 1 -> ?)
# we can select one element from that dimension and write to it
# to achieve writing to all values of that dimension of the input tensor
def get_expanded_dims(t):
    if not isinstance(t, torch.Tensor):
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 806.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 806.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 806.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x2fa26f967cb80c6f`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


>>>>>>> b
class _TensorLoader(ABC):
```

</td>
<td valign="top">

```python
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass
```

</td>
<td valign="top">

```python
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass
```

</td>
<td valign="top">

```python
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 512.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 512.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 512.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


>>>>>>> b
class _TensorLoader(ABC):
```

</td>
<td valign="top">

```python
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass

    @abstractmethod
```

</td>
<td valign="top">

```python
def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )


class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass

    @abstractmethod
```

</td>
<td valign="top">

```python
class _TensorLoader(ABC):
    @abstractmethod
    def add(self, size: int, obj: object) -> None:
        pass

    @abstractmethod

def _trim(tensor: torch.Tensor) -> torch.Tensor:
    tensor = tensor.detach().cpu()
    if tensor._typed_storage()._size() != tensor.numel():
        tensor = tensor.clone()
    return tensor


def _result_from_write_item(
    item: WriteItem, size_in_bytes, storage_data
) -> WriteResult:
    return WriteResult(
        index=item.index, size_in_bytes=size_in_bytes, storage_data=storage_data
    )
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 533.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 533.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 532.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
