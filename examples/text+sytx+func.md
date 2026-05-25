# `text+sytx+func` bucket — worked examples

All three aspects differ in the same conflict region — the hardest bucket. Distributions are bimodal (peaks near 0 and near 1).

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0xf71ef4bd373cf765`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.171)</th>
<th align="left">v2-sys (max=0.163)</th>
<th align="left">v2.1-sys (max=1.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

=======
>>>>>>> b

```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        # Example usage of the function
        result = fn(torch.randn(2, 10), torch.randn(2, 10))
        self.assertTrue(torch.allclose(result, torch.cos(torch.randn(2, 10)) + torch.randn(2, 10), atol=1e-5))
```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        # Example usage
        result = fn(torch.randn(2, 10), torch.randn(2, 10))
        # Verify the result
        self.assertTrue(torch.allclose(result, result, atol=1e-5))
```

</td>
<td valign="top">

```python
def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")
```

</td>
<td valign="top">

```python

    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.3× under-gen &nbsp;·&nbsp; max=**0.171**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.3× under-gen &nbsp;·&nbsp; max=**0.163**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**1.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.303)</th>
<th align="left">v2-sys (max=0.101)</th>
<th align="left">v2.1-sys (max=0.948)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

=======
>>>>>>> b

```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        model = torch.nn.Sequential(fn)
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend="aot_eager")(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))
```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
```

</td>
<td valign="top">

```python
def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
```

</td>
<td valign="top">

```python

    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.3× under-gen &nbsp;·&nbsp; max=**0.303**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.101**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.948**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x1a8336140eb8aa8b`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.176)</th>
<th align="left">v2-sys (max=0.163)</th>
<th align="left">v2.1-sys (max=1.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

=======
>>>>>>> b

```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        # Example usage of the function
        result = fn(torch.randn(2, 10), torch.randn(2, 10))
        # Verify the result
        self.assertTrue(torch.allclose(result, torch.cos(torch.randn(2, 10)) + torch.randn(2, 10), atol=1e-5))
```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        # Example usage
        result = fn(torch.randn(2, 10), torch.randn(2, 10))
        # Verify the result
        self.assertTrue(torch.allclose(result, result, atol=1e-5))
```

</td>
<td valign="top">

```python
def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")
```

</td>
<td valign="top">

```python

    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.4× under-gen &nbsp;·&nbsp; max=**0.176**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.3× under-gen &nbsp;·&nbsp; max=**0.163**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**1.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.303)</th>
<th align="left">v2-sys (max=0.101)</th>
<th align="left">v2.1-sys (max=0.948)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

=======
>>>>>>> b

```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
        model = torch.nn.Sequential(fn)
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend="aot_eager")(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))
```

</td>
<td valign="top">

```python
class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
```

</td>
<td valign="top">

```python
def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

class NormalizeIRTests(torch._dynamo.test_case.TestCase):
    def test_inplace_normalize(self):
        def fn(a, b):
            x = torch.cos(a)
            x += b
```

</td>
<td valign="top">

```python

    def _check_backend_works(self, backend):
        model = Seq().eval()
        input = torch.randn(2, 10)
        r1 = model(input)
        r2 = torch.compile(model, backend=backend)(input)
        self.assertTrue(same(r1, r2.float(), tol=0.01))

    def test_eager(self):
        self._check_backend_works("eager")

    def test_torchscript(self):
        self._check_backend_works("ts")

    def test_aot_eager(self):
        self._check_backend_works("aot_eager")

    def test_aot_eager_decomp_partition(self):
        self._check_backend_works("aot_eager_decomp_partition")

    def test_aot_cudagraphs(self):
        self._check_backend_works("cudagraphs")

    def test_aot_ts(self):
        self._check_backend_works("aot_ts")

    def test_aot_ts_nvfuser(self):
        self._check_backend_works("aot_ts_nvfuser")

    def test_nvprims_nvfuser(self):
        self._check_backend_works("nvprims_nvfuser")

    def test_nvprims_aten(self):
        self._check_backend_works("nvprims_aten")

    @unittest.skipIf(not has_onnxruntime(), "requires onnxruntime")
    def test_onnxrt(self):
        self._check_backend_works("onnxrt")

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.3× under-gen &nbsp;·&nbsp; max=**0.303**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.101**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.948**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0xe10d686ec92e9f91`

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
# Not actually a view!
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


# Not actually a view!
class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None


>>>>>>> b
# Need to make it obvious that users should be passing in offsets
```

</td>
<td valign="top">

```python
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )

class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None

# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
):
    if offsets is None:
        raise ValueError("Offsets must be provided")
    return NestedTensor(
        torch.stack(tensors, dim=0).detach(),
        offsets=offsets,
    )
```

</td>
<td valign="top">

```python
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )

class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None

# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
):
    if offsets is None:
        offsets = torch.tensor([0] * len(tensors), dtype=torch.int64, device=device)
    return NestedTensor(
        torch.stack(tensors, dim=0).detach(),
        offsets=offsets,
    )
```

</td>
<td valign="top">

```python
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None


# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
):
    if offsets is None:
        offsets = torch.tensor([0] * len(tensors), dtype=torch.long, device=device)
    return NestedTensor(
        torch.stack(tensors, dim=0),
        offsets=offsets,
        dtype=dtype,
        device=device,
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

**custom** &nbsp;·&nbsp; 1342.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1374.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1938.0× over-gen &nbsp;·&nbsp; max=**0.000**

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
# Not actually a view!
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


# Not actually a view!
class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None


>>>>>>> b
# Need to make it obvious that users should be passing in offsets
```

</td>
<td valign="top">

```python
pass
        with torch._C.DisableTorchFunctionSubclass():
            return func(*args, **kwargs)

# Not actually a view!
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


# Not actually a view!
class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None


# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
```

</td>
<td valign="top">

```python
pass
        with torch._C.DisableTorchFunctionSubclass():
            return func(*args, **kwargs)


# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
)


# Not actually a view!
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


# Not actually a view!
class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None
```

</td>
<td valign="top">

```python
pass
        with torch._C.DisableTorchFunctionSubclass():
            return func(*args, **kwargs)


# Not actually a view!
class ViewBufferFromNested(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: NestedTensor):  # type: ignore[override]
        ctx.save_for_backward(x.offsets())
        ctx.metadata_cache = x._metadata_cache
        ctx.ragged_idx = x._ragged_idx
        return x.values()

    @staticmethod
    def backward(ctx, gO: torch.Tensor):  # type: ignore[override]
        (offsets,) = ctx.saved_tensors
        return NestedTensor(
            gO,
            offsets=offsets,
            _metadata_cache=ctx.metadata_cache,
            _ragged_idx=ctx.ragged_idx,
        )


# Not actually a view!
class ViewNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None


# Not actually a view!
# NOTE: @jbschlosser is working on making it a view
class ViewNonContiguousNestedFromBuffer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values: torch.Tensor, offsets: torch.Tensor, lengths: torch.Tensor):  # type: ignore[override]
        return NestedTensor(
            values.detach(),
            offsets=offsets,
            lengths=lengths,
        )

    @staticmethod
    def backward(ctx, gO: NestedTensor):  # type: ignore[override]
        return gO.values(), None, None


# Need to make it obvious that users should be passing in offsets
def jagged_from_list(
    tensors: List[torch.Tensor],
    offsets: Optional[torch.Tensor],
    dtype=None,
    device=None,
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

**pick-b** &nbsp;·&nbsp; 1837.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 1840.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 1838.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x3936d49f05be7354`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.071)</th>
<th align="left">v2-sys (max=0.071)</th>
<th align="left">v2.1-sys (max=0.071)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)
=======
>>>>>>> b

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

```

</td>
<td valign="top">

```python
class TorchBindOpOverload(OpOverload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op
        register_side_effect_op(self)

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
        if any(isinstance(x, FakeScriptObject) for x in args + kwargs.values()):
            return self._get_dispatch(self_, *args, **kwargs)
        else:
            return self._get_dispatch(self_, *args, **kwargs)
```

</td>
<td valign="top">

```python
class TorchBindOpOverload(OpOverload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
        if any(isinstance(x, FakeScriptObject) for x in args + kwargs.values()):
            return self._get_dispatch(self_, *args, **kwargs)
        else:
            return self._dispatch(self_, *args, **kwargs)
```

</td>
<td valign="top">

```python
class TorchBindOpOverload(OpOverload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
        if any(isinstance(x, FakeScriptObject) for x in args + kwargs.values()):
            return self._get_dispatch(self_, *args, **kwargs)
        else:
            return self._get_dispatch(self_, *args, **kwargs)
```

</td>
<td valign="top">

```python
        for key in [
            DispatchKey.Autograd,
            DispatchKey.ADInplaceOrView,
            DispatchKey.PythonTLSSnapshot,
        ]:
            self.py_impl(key)(torch.library.fallthrough_kernel)

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 10.1× over-gen &nbsp;·&nbsp; max=**0.071**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 10.1× over-gen &nbsp;·&nbsp; max=**0.071**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 10.1× over-gen &nbsp;·&nbsp; max=**0.071**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.076)</th>
<th align="left">v2-sys (max=0.082)</th>
<th align="left">v2.1-sys (max=0.082)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)
=======
>>>>>>> b

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

```

</td>
<td valign="top">

```python
class TorchBindOpOverload(OpOverload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)

    # Note: we automatically add implementations for modes that are useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidentally trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
```

</td>
<td valign="top">

```python
# All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
```

</td>
<td valign="top">

```python
# All torchbind op are considered as having side-effects
        from torch._higher_order_ops.effects import register_side_effect_op

        register_side_effect_op(self)

    # Note: we automaticallly add implementations for modes that useful for tracing.
    # We only add implementation when we must dispatch in python by checking the inputs.
    # We cannot do it before seeing the inputs because some torch bind ops
    # (e.g. profiler record function) might be registered globally
    # with a single default implementation in cpp. We might accidently trace them
    # into graph.
    @contextlib.contextmanager
    def _maybe_py_impl_default_dispatch_mode(self):
        def wrapper(mode, *args, **kwargs):
            return _mannually_invoke_dispatch_mode_in_python(
                mode, self, *args, **kwargs
            )

        modes = [
            torch._subclasses.functional_tensor.FunctionalTensorMode,
            torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode,
            torch._subclasses.fake_tensor.FakeTensorMode,
        ]
        default_impl_modes = []
        try:
            for mode in modes:
                if mode not in self.python_key_mode_table:
                    self.py_impl(mode)(wrapper)
                    default_impl_modes.append(mode)
            yield
        finally:
            for mode in default_impl_modes:
                del self.python_key_mode_table[mode]
                self._dispatch_cache.clear()

    # use `self_` to avoid naming collide with arguments that
    # are named "self". This way, they can be called by kwargs.
    def __call__(self_, *args, **kwargs):  # noqa: B902
        # The path when any inputs are FakeScriptObject, we need to
        # skip c++ dispatcher and dispatch in python through _get_dispatch of python_dispatcher.
```

</td>
<td valign="top">

```python
        for key in [
            DispatchKey.Autograd,
            DispatchKey.ADInplaceOrView,
            DispatchKey.PythonTLSSnapshot,
        ]:
            self.py_impl(key)(torch.library.fallthrough_kernel)

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 9.1× over-gen &nbsp;·&nbsp; max=**0.076**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 8.5× over-gen &nbsp;·&nbsp; max=**0.082**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 8.5× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.082**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
