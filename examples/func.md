# `func` bucket — worked examples

ConGra `func` cases involve **changes that alter program behavior** — added/removed control flow, asserts, branches. The headline behaviour in our pilots is that these cases (a) have short ground truths, so length-mismatch penalties bite hard, and (b) often need a *combine* of both sides because each side touched a different concern.

---

## Case `0xc99534a64262c8c6`

Apertus v1 took side `b` only and missed all of side `a` (max=0.243); v2's output-discipline rules pushed it to combine both sides correctly (max=0.847, v2.1 identical). Qwen3 v1 already combined correctly (max=0.713); v2.1 oddly regressed Qwen3 back to v1's incomplete output.

### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.243)</th>
<th align="left">v2-sys (max=0.847)</th>
<th align="left">v2.1-sys (max=0.847)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a

        data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

=======
>>>>>>> b
        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
v = ssl.RAND_status()
        if support.verbose:
            sys.stdout.write("\n RAND_status is %d (%s)\n"
                             % (v, (v and "sufficient randomness") or
                                "insufficient randomness"))

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
                                "insufficient randomness"))

        data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        self.assertRaises(TypeError, ssl.RAND_egd, 1)
        self.assertRaises(TypeError, ssl.RAND_egd, 'foo', 1)
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
</tr>
</table>

### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.713)</th>
<th align="left">v2-sys (max=0.847)</th>
<th align="left">v2.1-sys (max=0.713)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a

        data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

=======
>>>>>>> b
        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)

    def test_parse_cert(self):
        # note that this uses an 'unofficial' function in _ssl.c,
        # provided solely for this test, to exercise the certificate
        # parsing code
```

</td>
<td valign="top">

```python
data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
<td valign="top">

```python
data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        try:
            ssl.RAND_egd(1)
        except TypeError:
            pass
        else:
            print("didn't raise TypeError")
        ssl.RAND_add("this is a random string", 75.0)

    def test_parse_cert(self):
        # note that this uses an 'unofficial' function in _ssl.c,
        # provided solely for this test, to exercise the certificate
        # parsing code
```

</td>
<td valign="top">

```python
                                "insufficient randomness"))

        data, is_cryptographic = ssl.RAND_pseudo_bytes(16)
        self.assertEqual(len(data), 16)
        self.assertEqual(is_cryptographic, v == 1)
        if v:
            data = ssl.RAND_bytes(16)
            self.assertEqual(len(data), 16)
        else:
            self.assertRaises(ssl.SSLError, ssl.RAND_bytes, 16)

        self.assertRaises(TypeError, ssl.RAND_egd, 1)
        self.assertRaises(TypeError, ssl.RAND_egd, 'foo', 1)
        ssl.RAND_add("this is a random string", 75.0)
```

</td>
</tr>
</table>

### Reading the row

- **Apertus v1** chose to retain only side `b` (the `try/except`) and dropped side `a`'s entire `RAND_pseudo_bytes` test block — a pure pick that was wrong (the GT keeps both). max=0.243.
- **Apertus v2 / v2.1** combine both sides — the correct *combine* pattern — and score 0.847. The remaining 0.15 is the GT's final `self.assertRaises(TypeError, ssl.RAND_egd, ...)` lines, which both models replaced with the simpler `try/except` from side b.
- **Qwen3 v1** already produces the *combine* output but over-generates `test_parse_cert` from surrounding context (max=0.713 — length penalty bites).
- **Qwen3 v2** trims the over-generation (max=0.847, same as Apertus v2).
- **Qwen3 v2.1** *regresses* — back to v1's over-generated output. v2.1's amplified output-discipline framing seems to confuse Qwen3 on cases where v1 already had a usable answer.
