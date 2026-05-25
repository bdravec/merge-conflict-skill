# `func` bucket — worked examples

Changes that **alter program behaviour** — added/removed control flow, asserts, branches. Short ground truths in this bucket make the length-mismatch penalty bite hard.

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0xc99534a64262c8c6`

#### Apertus-8B

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
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.243**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.847**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.847**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

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
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.713**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.847**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.713**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x41aeb55e06c120e6`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.846)</th>
<th align="left">v2-sys (max=0.762)</th>
<th align="left">v2.1-sys (max=0.867)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
=======
>>>>>>> b
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
elif isinstance(value, (torch.fx.graph_module.GraphModule, torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        else:
            return UserDefinedObjectVariable(value)
```

</td>
<td valign="top">

```python
elif isinstance(value, (torch.fx.graph_module.GraphModule, 
                                torch.utils._pytree.TreeSpec, 
                                torch.utils._pytree.LeafSpec)):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, torch.utils._pytree.TreeSpec) or \
                isinstance(value, torch.utils._pytree.LeafSpec):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(value, types.MethodWrapperType):
            return MethodWrapperVariable(value)
        elif isinstance(value, (tuple, list)):
            cls = BaseListVariable.cls_for(type(value))
            return cls([self(tx, x) for x in value], mutable_local=MutableLocal())
        else:
            return UnimplementedVariable(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
elif isinstance(value, (torch.fx.graph_module.GraphModule, 
                                torch.utils._pytree.TreeSpec, 
                                torch.utils._pytree.LeafSpec)):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        else:
            unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
            return MethodWrapperVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        elif PlacementVariable.is_placement(value):
            return PlacementVariable(value)
        elif DeviceMeshVariable.is_device_mesh(value):
            return DeviceMeshVariable(value)
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.846**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1.5× over-gen &nbsp;·&nbsp; max=**0.762**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.867**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.717)</th>
<th align="left">v2-sys (max=0.859)</th>
<th align="left">v2.1-sys (max=0.852)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
=======
>>>>>>> b
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
elif isinstance(value, (tuple, list)):
            cls = BaseListVariable.cls_for(type(value))
            return cls([self(tx, x) for x in value], mutable_local=MutableLocal())
        elif isinstance(value, types.MethodWrapperType):
            return MethodWrapperVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")

    @staticmethod
    def wrap_constant_literal(value):
        assert ConstantVariable.is_literal(value)
        return ConstantVariable.create(value=value)
```

</td>
<td valign="top">

```python
elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        elif isinstance(value, types.MethodWrapperType):
            return MethodWrapperVariable(value)
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
<td valign="top">

```python
            return MethodWrapperVariable(value)
        elif isinstance(value, torch.fx.graph_module.GraphModule):
            return SourcelessGraphModuleVariable(value)
        elif isinstance(
            value, (torch.utils._pytree.TreeSpec, torch.utils._pytree.LeafSpec)
        ):
            return UserDefinedObjectVariable(value)
        elif PlacementVariable.is_placement(value):
            return PlacementVariable(value)
        elif DeviceMeshVariable.is_device_mesh(value):
            return DeviceMeshVariable(value)
        unimplemented(f"Unexpected type in sourceless builder {type(value)}")
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.717**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.859**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.852**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0xee1a814e473f57ee`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.029)</th>
<th align="left">v2-sys (max=0.020)</th>
<th align="left">v2.1-sys (max=0.020)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python


class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
<<<<<<< a
            onnx_model,
            self._input_adapter,
            self._output_adapter,
            self.options.diagnostics_context,
=======
            onnx_model, self._input_adapter, self._output_adapter
>>>>>>> b
        )

```

</td>
<td valign="top">

```python
self._input_adapter,
                self._output_adapter,
            )
        return flattened_outputs


class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model,
            self._input_adapter,
            self._output_adapter,
            self.options.diagnostics_context,
        )
```

</td>
<td valign="top">

```python
class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model,
            self._input_adapter,
            self._output_adapter,
            self.options.diagnostics_context,
        )
```

</td>
<td valign="top">

```python
class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model,
            self._input_adapter,
            self._output_adapter,
            self.options.diagnostics_context,
        )
```

</td>
<td valign="top">

```python
        return flattened_outputs
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 151.7× over-gen &nbsp;·&nbsp; max=**0.029**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 148.3× over-gen &nbsp;·&nbsp; max=**0.020**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 148.3× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.020**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.020)</th>
<th align="left">v2-sys (max=0.099)</th>
<th align="left">v2.1-sys (max=0.021)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python


class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
<<<<<<< a
            onnx_model,
            self._input_adapter,
            self._output_adapter,
            self.options.diagnostics_context,
=======
            onnx_model, self._input_adapter, self._output_adapter
>>>>>>> b
        )

```

</td>
<td valign="top">

```python
class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model, self._input_adapter, self._output_adapter, self.options.diagnostics_context
        )
```

</td>
<td valign="top">

```python
# Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model, self._input_adapter, self._output_adapter
        )
```

</td>
<td valign="top">

```python
class FXGraphModuleExporter(exporter.Exporter, abc.ABC):
    _input_adapter: exporter.InputAdapter
    _output_adapter: exporter.OutputAdapter

    @property
    def decomposition_table(self) -> Mapping[torch._ops.OpOverload, Callable]:
        return function_dispatcher._ONNX_FRIENDLY_DECOMPOSITION_TABLE

    def _apply_input_adapt_step(
        self,
        adapt_step_cls: Type[exporter.InputAdaptStep],
        model_args: Sequence[Any],
        model_kwargs: Mapping[str, Any],
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Tuple[Sequence[Any], Mapping[str, Any]]:
        """Apply an input adapt step to the model args and kwargs.

        An input adapt step object is initialized, applied and recorded as part of
        ``self._input_adapter`.

        Args:
            adapt_step_cls: The input adapt step class.
            model_args: The model args.
            model_kwargs: The model kwargs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model args and kwargs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._input_adapter.append_step(adapt_step)
        return adapt_step.apply(model_args, model_kwargs)

    def _apply_output_adapt_step(
        self,
        adapt_step_cls: Type[exporter.OutputAdaptStep],
        model_outputs: Any,
        step_init_args: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Apply an output adapt step to the model outputs.

        An output adapt step object is initialized, applied and recorded as part of
        ``self._output_adapter`.

        Args:
            adapt_step_cls: The output adapt step class.
            model_outputs: The model outputs.
            step_init_args: The input adapt step initialization arguments.

        Returns:
            The adapted model outputs.
        """
        step_init_args = step_init_args or ()
        adapt_step = adapt_step_cls(*step_init_args)
        self._output_adapter.append_step(adapt_step)
        return adapt_step.apply(model_outputs)

    @_beartype.beartype
    def export_fx_to_onnx(
        self,
        fx_module: torch.fx.GraphModule,
        fx_module_args: Sequence[Any],
    ) -> torch.onnx.ExportOutput:
        # Apply decomposition table to the input graph.
        module = passes.Decompose(
            fx_module,
            self.decomposition_table,
            enable_dynamic_axes=self.options.dynamic_shapes,
        ).run(*fx_module_args)

        # ONNX does not support views and mutations.
        # Functionalize to get a semantically equivalent graph without mutations.
        module = passes.Functionalize(
            module, enable_dynamic_axes=self.options.dynamic_shapes
        ).run(*fx_module_args)
        # Input mutations are detected and distilled after `Functionalize` pass.
        # Remove them since ONNX inference does not need them.
        module = passes.RemoveInputMutation(module).run(*fx_module_args)

        # Run ShapeInferenceWithFakeTensor to get static shape of nodes for op_level_debug purposes
        # The pass added nodes with static shape into original node metadata:
        # node.meta["static_shape"]: FakeTensor/int/float/SymInt/SynFloat
        if self.options.op_level_debug:
            module = passes.ShapeInferenceWithFakeTensor(module).run(*fx_module_args)

        # We want to pass list of ints and floats to TorchScript graph correctly
        # in _export_fx_to_ts, so we must disable FakeTensorMode. Otherwise, graph may
        # receive FakeTensor and results runtime error. In addition, TorchScript-based
        # ONNX exporter used in _ts_graph_to_onnx_model_in_protobuf is not compatible
        # with FakeTensorMode.
        with torch.utils._mode_utils.no_dispatch():
            onnxscript_graph = passes.export_fx_to_onnxscript(module, self.options)
            # ONNX does not support None inputs. During graph building, all None inputs
            # are removed. Here we register this step to input adapter.
            self._apply_input_adapt_step(RemoveNoneInputStep, fx_module_args, {})
            # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
            # tensor, etc), we flatten the collection and register each element as output.
            self._output_adapter.append_step(FlattenOutputStep())

        # Export TorchScript graph to ONNX ModelProto.
        onnx_model = onnxscript_graph.to_model_proto(self.options.opset_version)
        return torch.onnx.ExportOutput(
            onnx_model, self._input_adapter, self._output_adapter
        )
```

</td>
<td valign="top">

```python
        return flattened_outputs
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 147.2× over-gen &nbsp;·&nbsp; max=**0.020**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 7.6× over-gen &nbsp;·&nbsp; max=**0.099**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 146.1× over-gen &nbsp;·&nbsp; max=**0.021**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x4c72bd7b3ad2343b`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.043)</th>
<th align="left">v2.1-sys (max=0.045)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
	def _readOptions(filename_bytes):
		try:
			optionf = open(filename_bytes)
		except IOError:
			return [] # silently skip if file is not present
		try:
			res = []
			for l in optionf:
				res += shlex.split(l, comments=True)
		finally:
			optionf.close()
		return res

	def _format_option_string(option):
		''' ('-o', '--option') -> -o, --format METAVAR'''

		opts = []

		if option._short_opts: opts.append(option._short_opts[0])
		if option._long_opts: opts.append(option._long_opts[0])
		if len(opts) > 1: opts.insert(1, ', ')

		if option.takes_value(): opts.append(' %s' % option.metavar)

		return "".join(opts)

	def _find_term_columns():
		columns = os.environ.get('COLUMNS', None)
		if columns:
			return int(columns)

		try:
			sp = subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err = sp.communicate()
			return int(out.split()[1])
		except:
			pass
		return None

	max_width = 80
	max_help_position = 80

	# No need to wrap help messages if we're on a wide console
	columns = _find_term_columns()
	if columns: max_width = columns

	fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)
	fmt.format_option_strings = _format_option_string

	kw = {
		'version'   : __version__,
		'formatter' : fmt,
		'usage' : '%prog [options] url [url...]',
		'conflict_handler' : 'resolve',
	}

	parser = optparse.OptionParser(**kw)

	# option groups
	general        = optparse.OptionGroup(parser, 'General Options')
	selection      = optparse.OptionGroup(parser, 'Video Selection')
	authentication = optparse.OptionGroup(parser, 'Authentication Options')
	video_format   = optparse.OptionGroup(parser, 'Video Format Options')
	postproc       = optparse.OptionGroup(parser, 'Post-processing Options')
	filesystem     = optparse.OptionGroup(parser, 'Filesystem Options')
	verbosity      = optparse.OptionGroup(parser, 'Verbosity / Simulation Options')

	general.add_option('-h', '--help',
			action='help', help='print this help text and exit')
	general.add_option('-v', '--version',
			action='version', help='print program version and exit')
	general.add_option('-U', '--update',
			action='store_true', dest='update_self', help='update this program to latest version')
	general.add_option('-i', '--ignore-errors',
			action='store_true', dest='ignoreerrors', help='continue on download errors', default=False)
	general.add_option('-r', '--rate-limit',
			dest='ratelimit', metavar='LIMIT', help='download rate limit (e.g. 50k or 44.6m)')
	general.add_option('-R', '--retries',
			dest='retries', metavar='RETRIES', help='number of retries (default is %default)', default=10)
	general.add_option('--dump-user-agent',
			action='store_true', dest='dump_user_agent',
			help='display the current browser identification', default=False)
	general.add_option('--user-agent',
			dest='user_agent', help='specify a custom user agent', metavar='UA')
	general.add_option('--list-extractors',
			action='store_true', dest='list_extractors',
			help='List all supported extractors and the URLs they would handle', default=False)

	selection.add_option('--playlist-start',
			dest='playliststart', metavar='NUMBER', help='playlist video to start at (default is %default)', default=1)
	selection.add_option('--playlist-end',
			dest='playlistend', metavar='NUMBER', help='playlist video to end at (default is last)', default=-1)
	selection.add_option('--match-title', dest='matchtitle', metavar='REGEX',help='download only matching titles (regex or caseless sub-string)')
	selection.add_option('--reject-title', dest='rejecttitle', metavar='REGEX',help='skip download for matching titles (regex or caseless sub-string)')
	selection.add_option('--max-downloads', metavar='NUMBER', dest='max_downloads', help='Abort after downloading NUMBER files', default=None)

	authentication.add_option('-u', '--username',
			dest='username', metavar='USERNAME', help='account username')
	authentication.add_option('-p', '--password',
			dest='password', metavar='PASSWORD', help='account password')
	authentication.add_option('-n', '--netrc',
			action='store_true', dest='usenetrc', help='use .netrc authentication data', default=False)


	video_format.add_option('-f', '--format',
			action='store', dest='format', metavar='FORMAT', help='video format code')
	video_format.add_option('--all-formats',
			action='store_const', dest='format', help='download all available video formats', const='all')
	video_format.add_option('--prefer-free-formats',
			action='store_true', dest='prefer_free_formats', default=False, help='prefer free video formats unless a specific one is requested')
	video_format.add_option('--max-quality',
			action='store', dest='format_limit', metavar='FORMAT', help='highest quality format to download')
	video_format.add_option('-F', '--list-formats',
			action='store_true', dest='listformats', help='list all available formats (currently youtube only)')
	video_format.add_option('--write-srt',
			action='store_true', dest='writesubtitles',
			help='write video closed captions to a .srt file (currently youtube only)', default=False)
	video_format.add_option('--srt-lang',
			action='store', dest='subtitleslang', metavar='LANG',
			help='language of the closed captions to download (optional) use IETF language tags like \'en\'')


	verbosity.add_option('-q', '--quiet',
			action='store_true', dest='quiet', help='activates quiet mode', default=False)
	verbosity.add_option('-s', '--simulate',
			action='store_true', dest='simulate', help='do not download the video and do not write anything to disk', default=False)
	verbosity.add_option('--skip-download',
			action='store_true', dest='skip_download', help='do not download the video', default=False)
	verbosity.add_option('-g', '--get-url',
			action='store_true', dest='geturl', help='simulate, quiet but print URL', default=False)
	verbosity.add_option('-e', '--get-title',
			action='store_true', dest='gettitle', help='simulate, quiet but print title', default=False)
	verbosity.add_option('--get-thumbnail',
			action='store_true', dest='getthumbnail',
			help='simulate, quiet but print thumbnail URL', default=False)
	verbosity.add_option('--get-description',
			action='store_true', dest='getdescription',
			help='simulate, quiet but print video description', default=False)
	verbosity.add_option('--get-filename',
			action='store_true', dest='getfilename',
			help='simulate, quiet but print output filename', default=False)
	verbosity.add_option('--get-format',
			action='store_true', dest='getformat',
			help='simulate, quiet but print output format', default=False)
	verbosity.add_option('--no-progress',
			action='store_true', dest='noprogress', help='do not print progress bar', default=False)
	verbosity.add_option('--console-title',
			action='store_true', dest='consoletitle',
			help='display progress in console titlebar', default=False)
	verbosity.add_option('-v', '--verbose',
			action='store_true', dest='verbose', help='print various debugging information', default=False)


	filesystem.add_option('-t', '--title',
			action='store_true', dest='usetitle', help='use title in file name', default=False)
	filesystem.add_option('--id',
			action='store_true', dest='useid', help='use video ID in file name', default=False)
	filesystem.add_option('-l', '--literal',
			action='store_true', dest='useliteral', help='use literal title in file name', default=False)
	filesystem.add_option('-A', '--auto-number',
			action='store_true', dest='autonumber',
			help='number downloaded files starting from 00000', default=False)
	filesystem.add_option('-o', '--output',
			dest='outtmpl', metavar='TEMPLATE', help='output filename template. Use %(stitle)s to get the title, %(uploader)s for the uploader name, %(autonumber)s to get an automatically incremented number, %(ext)s for the filename extension, %(upload_date)s for the upload date (YYYYMMDD), %(extractor)s for the provider (youtube, metacafe, etc), %(id)s for the video id and %% for a literal percent. Use - to output to stdout.')
	filesystem.add_option('-a', '--batch-file',
			dest='batchfile', metavar='FILE', help='file containing URLs to download (\'-\' for stdin)')
	filesystem.add_option('-w', '--no-overwrites',
			action='store_true', dest='nooverwrites', help='do not overwrite files', default=False)
	filesystem.add_option('-c', '--continue',
			action='store_true', dest='continue_dl', help='resume partially downloaded files', default=True)
	filesystem.add_option('--no-continue',
			action='store_false', dest='continue_dl',
			help='do not resume partially downloaded files (restart from beginning)')
	filesystem.add_option('--cookies',
			dest='cookiefile', metavar='FILE', help='file to read cookies from and dump cookie jar in')
	filesystem.add_option('--no-part',
			action='store_true', dest='nopart', help='do not use .part files', default=False)
	filesystem.add_option('--no-mtime',
			action='store_false', dest='updatetime',
			help='do not use the Last-modified header to set the file modification time', default=True)
	filesystem.add_option('--write-description',
			action='store_true', dest='writedescription',
			help='write video description to a .description file', default=False)
	filesystem.add_option('--write-info-json',
			action='store_true', dest='writeinfojson',
			help='write video metadata to a .info.json file', default=False)


	postproc.add_option('-x', '--extract-audio', action='store_true', dest='extractaudio', default=False,
			help='convert video files to audio-only files (requires ffmpeg or avconv and ffprobe or avprobe)')
	postproc.add_option('--audio-format', metavar='FORMAT', dest='audioformat', default='best',
			help='"best", "aac", "vorbis", "mp3", "m4a", or "wav"; best by default')
	postproc.add_option('--audio-quality', metavar='QUALITY', dest='audioquality', default='5',
			help='ffmpeg/avconv audio quality specification, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)')
	postproc.add_option('-k', '--keep-video', action='store_true', dest='keepvideo', default=False,
			help='keeps the video file on disk after the post-processing; the video is erased by default')


	parser.add_option_group(general)
	parser.add_option_group(selection)
	parser.add_option_group(filesystem)
	parser.add_option_group(verbosity)
	parser.add_option_group(video_format)
	parser.add_option_group(authentication)
	parser.add_option_group(postproc)

	xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
	if xdg_config_home:
		userConf = os.path.join(xdg_config_home, 'youtube-dl.conf')
	else:
		userConf = os.path.join(os.path.expanduser('~'), '.config', 'youtube-dl.conf')
	argv = _readOptions('/etc/youtube-dl.conf') + _readOptions(userConf) + sys.argv[1:]
	opts, args = parser.parse_args(argv)

	return parser, opts, args

def gen_extractors():
	""" Return a list of an instance of every supported extractor.
	The order does matter; the first extractor matched is the one handling the URL.
	"""
	return [
		YoutubePlaylistIE(),
		YoutubeChannelIE(),
		YoutubeUserIE(),
		YoutubeSearchIE(),
		YoutubeIE(),
		MetacafeIE(),
		DailymotionIE(),
		GoogleIE(),
		GoogleSearchIE(),
		PhotobucketIE(),
		YahooIE(),
		YahooSearchIE(),
		DepositFilesIE(),
		FacebookIE(),
		BlipTVUserIE(),
		BlipTVIE(),
		VimeoIE(),
		MyVideoIE(),
		ComedyCentralIE(),
		EscapistIE(),
		CollegeHumorIE(),
		XVideosIE(),
		SoundcloudIE(),
		InfoQIE(),
		MixcloudIE(),
		StanfordOpenClassroomIE(),
		MTVIE(),
		YoukuIE(),
		XNXXIE(),
		GooglePlusIE(),
<<<<<<< a
		PornotubeIE(),
		YouPornIE(),
		YouJizzIE(),
=======

>>>>>>> b
		GenericIE()
	]

```

</td>
<td valign="top">

```python

```

</td>
<td valign="top">

```python
def gen_extractors():
    """ Return a list of an instance of every supported extractor.
    The order does matter; the first extractor matched is the one handling the URL.
    """
    return [
        YoutubePlaylistIE(),
        YoutubeChannelIE(),
        YoutubeUserIE(),
        YoutubeSearchIE(),
        YoutubeIE(),
        MetacafeIE(),
        DailymotionIE(),
        GoogleIE(),
        GoogleSearchIE(),
        PhotobucketIE(),
        YahooIE(),
        YahooSearchIE(),
        DepositFilesIE(),
        FacebookIE(),
        BlipTVUserIE(),
        BlipTVIE(),
        VimeoIE(),
        MyVideoIE(),
        ComedyCentralIE(),
        EscapistIE(),
        CollegeHumorIE(),
        XVideosIE(),
        SoundcloudIE(),
        InfoQIE(),
        MixcloudIE(),
        StanfordOpenClassroomIE(),
        MTVIE(),
        YoukuIE(),
        XNXXIE(),
        GooglePlusIE(),
        GenericIE()
    ]
```

</td>
<td valign="top">

```python
def gen_extractors():
    """ Return a list of an instance of every supported extractor.
    The order does matter; the first extractor matched is the one handling the URL.
    """
    return [
        YoutubePlaylistIE(),
        YoutubeChannelIE(),
        YoutubeUserIE(),
        YoutubeSearchIE(),
        YoutubeIE(),
        MetacafeIE(),
        DailymotionIE(),
        GoogleIE(),
        GoogleSearchIE(),
        PhotobucketIE(),
        YahooIE(),
        YahooSearchIE(),
        DepositFilesIE(),
        FacebookIE(),
        BlipTVUserIE(),
        BlipTVIE(),
        VimeoIE(),
        MyVideoIE(),
        ComedyCentralIE(),
        EscapistIE(),
        CollegeHumorIE(),
        XVideosIE(),
        SoundcloudIE(),
        InfoQIE(),
        MixcloudIE(),
        StanfordOpenClassroomIE(),
        MTVIE(),
        YoukuIE(),
        XNXXIE(),
        GooglePlusIE(),
        PornotubeIE(),
        YouPornIE(),
        YouJizzIE(),
        GenericIE()
    ]
```

</td>
<td valign="top">

```python
    def _readOptions(filename_bytes):
        try:
            optionf = open(filename_bytes)
        except IOError:
            return [] # silently skip if file is not present
        try:
            res = []
            for l in optionf:
                res += shlex.split(l, comments=True)
        finally:
            optionf.close()
        return res

    def _format_option_string(option):
        ''' ('-o', '--option') -> -o, --format METAVAR'''

        opts = []

        if option._short_opts:
            opts.append(option._short_opts[0])
        if option._long_opts:
            opts.append(option._long_opts[0])
        if len(opts) > 1:
            opts.insert(1, ', ')

        if option.takes_value(): opts.append(' %s' % option.metavar)

        return "".join(opts)

    def _find_term_columns():
        columns = os.environ.get('COLUMNS', None)
        if columns:
            return int(columns)

        try:
            sp = subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = sp.communicate()
            return int(out.split()[1])
        except:
            pass
        return None

    max_width = 80
    max_help_position = 80

    # No need to wrap help messages if we're on a wide console
    columns = _find_term_columns()
    if columns: max_width = columns

    fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)
    fmt.format_option_strings = _format_option_string

    kw = {
        'version'   : __version__,
        'formatter' : fmt,
        'usage' : '%prog [options] url [url...]',
        'conflict_handler' : 'resolve',
    }

    parser = optparse.OptionParser(**kw)

    # option groups
    general        = optparse.OptionGroup(parser, 'General Options')
    selection      = optparse.OptionGroup(parser, 'Video Selection')
    authentication = optparse.OptionGroup(parser, 'Authentication Options')
    video_format   = optparse.OptionGroup(parser, 'Video Format Options')
    postproc       = optparse.OptionGroup(parser, 'Post-processing Options')
    filesystem     = optparse.OptionGroup(parser, 'Filesystem Options')
    verbosity      = optparse.OptionGroup(parser, 'Verbosity / Simulation Options')

    general.add_option('-h', '--help',
            action='help', help='print this help text and exit')
    general.add_option('-v', '--version',
            action='version', help='print program version and exit')
    general.add_option('-U', '--update',
            action='store_true', dest='update_self', help='update this program to latest version')
    general.add_option('-i', '--ignore-errors',
            action='store_true', dest='ignoreerrors', help='continue on download errors', default=False)
    general.add_option('-r', '--rate-limit',
            dest='ratelimit', metavar='LIMIT', help='download rate limit (e.g. 50k or 44.6m)')
    general.add_option('-R', '--retries',
            dest='retries', metavar='RETRIES', help='number of retries (default is %default)', default=10)
    general.add_option('--buffer-size',
            dest='buffersize', metavar='SIZE', help='size of download buffer (e.g. 1024 or 16k) (default is %default)', default="1024")
    general.add_option('--no-resize-buffer',
            action='store_true', dest='noresizebuffer',
            help='do not automatically adjust the buffer size. By default, the buffer size is automatically resized from an initial value of SIZE.', default=False)
    general.add_option('--dump-user-agent',
            action='store_true', dest='dump_user_agent',
            help='display the current browser identification', default=False)
    general.add_option('--user-agent',
            dest='user_agent', help='specify a custom user agent', metavar='UA')
    general.add_option('--list-extractors',
            action='store_true', dest='list_extractors',
            help='List all supported extractors and the URLs they would handle', default=False)
    general.add_option('--test', action='store_true', dest='test', default=False, help=optparse.SUPPRESS_HELP)

    selection.add_option('--playlist-start',
            dest='playliststart', metavar='NUMBER', help='playlist video to start at (default is %default)', default=1)
    selection.add_option('--playlist-end',
            dest='playlistend', metavar='NUMBER', help='playlist video to end at (default is last)', default=-1)
    selection.add_option('--match-title', dest='matchtitle', metavar='REGEX',help='download only matching titles (regex or caseless sub-string)')
    selection.add_option('--reject-title', dest='rejecttitle', metavar='REGEX',help='skip download for matching titles (regex or caseless sub-string)')
    selection.add_option('--max-downloads', metavar='NUMBER', dest='max_downloads', help='Abort after downloading NUMBER files', default=None)

    authentication.add_option('-u', '--username',
            dest='username', metavar='USERNAME', help='account username')
    authentication.add_option('-p', '--password',
            dest='password', metavar='PASSWORD', help='account password')
    authentication.add_option('-n', '--netrc',
            action='store_true', dest='usenetrc', help='use .netrc authentication data', default=False)


    video_format.add_option('-f', '--format',
            action='store', dest='format', metavar='FORMAT', help='video format code')
    video_format.add_option('--all-formats',
            action='store_const', dest='format', help='download all available video formats', const='all')
    video_format.add_option('--prefer-free-formats',
            action='store_true', dest='prefer_free_formats', default=False, help='prefer free video formats unless a specific one is requested')
    video_format.add_option('--max-quality',
            action='store', dest='format_limit', metavar='FORMAT', help='highest quality format to download')
    video_format.add_option('-F', '--list-formats',
            action='store_true', dest='listformats', help='list all available formats (currently youtube only)')
    video_format.add_option('--write-srt',
            action='store_true', dest='writesubtitles',
            help='write video closed captions to a .srt file (currently youtube only)', default=False)
    video_format.add_option('--srt-lang',
            action='store', dest='subtitleslang', metavar='LANG',
            help='language of the closed captions to download (optional) use IETF language tags like \'en\'')


    verbosity.add_option('-q', '--quiet',
            action='store_true', dest='quiet', help='activates quiet mode', default=False)
    verbosity.add_option('-s', '--simulate',
            action='store_true', dest='simulate', help='do not download the video and do not write anything to disk', default=False)
    verbosity.add_option('--skip-download',
            action='store_true', dest='skip_download', help='do not download the video', default=False)
    verbosity.add_option('-g', '--get-url',
            action='store_true', dest='geturl', help='simulate, quiet but print URL', default=False)
    verbosity.add_option('-e', '--get-title',
            action='store_true', dest='gettitle', help='simulate, quiet but print title', default=False)
    verbosity.add_option('--get-thumbnail',
            action='store_true', dest='getthumbnail',
            help='simulate, quiet but print thumbnail URL', default=False)
    verbosity.add_option('--get-description',
            action='store_true', dest='getdescription',
            help='simulate, quiet but print video description', default=False)
    verbosity.add_option('--get-filename',
            action='store_true', dest='getfilename',
            help='simulate, quiet but print output filename', default=False)
    verbosity.add_option('--get-format',
            action='store_true', dest='getformat',
            help='simulate, quiet but print output format', default=False)
    verbosity.add_option('--no-progress',
            action='store_true', dest='noprogress', help='do not print progress bar', default=False)
    verbosity.add_option('--console-title',
            action='store_true', dest='consoletitle',
            help='display progress in console titlebar', default=False)
    verbosity.add_option('-v', '--verbose',
            action='store_true', dest='verbose', help='print various debugging information', default=False)


    filesystem.add_option('-t', '--title',
            action='store_true', dest='usetitle', help='use title in file name', default=False)
    filesystem.add_option('--id',
            action='store_true', dest='useid', help='use video ID in file name', default=False)
    filesystem.add_option('-l', '--literal',
            action='store_true', dest='usetitle', help='[deprecated] alias of --title', default=False)
    filesystem.add_option('-A', '--auto-number',
            action='store_true', dest='autonumber',
            help='number downloaded files starting from 00000', default=False)
    filesystem.add_option('-o', '--output',
            dest='outtmpl', metavar='TEMPLATE', help='output filename template. Use %(title)s to get the title, %(uploader)s for the uploader name, %(uploader_id)s for the uploader nickname if different, %(autonumber)s to get an automatically incremented number, %(ext)s for the filename extension, %(upload_date)s for the upload date (YYYYMMDD), %(extractor)s for the provider (youtube, metacafe, etc), %(id)s for the video id and %% for a literal percent. Use - to output to stdout. Can also be used to download to a different directory, for example with -o \'/my/downloads/%(uploader)s/%(title)s-%(id)s.%(ext)s\' .')
    filesystem.add_option('--restrict-filenames',
            action='store_true', dest='restrictfilenames',
            help='Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames', default=False)
    filesystem.add_option('-a', '--batch-file',
            dest='batchfile', metavar='FILE', help='file containing URLs to download (\'-\' for stdin)')
    filesystem.add_option('-w', '--no-overwrites',
            action='store_true', dest='nooverwrites', help='do not overwrite files', default=False)
    filesystem.add_option('-c', '--continue',
            action='store_true', dest='continue_dl', help='resume partially downloaded files', default=True)
    filesystem.add_option('--no-continue',
            action='store_false', dest='continue_dl',
            help='do not resume partially downloaded files (restart from beginning)')
    filesystem.add_option('--cookies',
            dest='cookiefile', metavar='FILE', help='file to read cookies from and dump cookie jar in')
    filesystem.add_option('--no-part',
            action='store_true', dest='nopart', help='do not use .part files', default=False)
    filesystem.add_option('--no-mtime',
            action='store_false', dest='updatetime',
            help='do not use the Last-modified header to set the file modification time', default=True)
    filesystem.add_option('--write-description',
            action='store_true', dest='writedescription',
            help='write video description to a .description file', default=False)
    filesystem.add_option('--write-info-json',
            action='store_true', dest='writeinfojson',
            help='write video metadata to a .info.json file', default=False)


    postproc.add_option('-x', '--extract-audio', action='store_true', dest='extractaudio', default=False,
            help='convert video files to audio-only files (requires ffmpeg or avconv and ffprobe or avprobe)')
    postproc.add_option('--audio-format', metavar='FORMAT', dest='audioformat', default='best',
            help='"best", "aac", "vorbis", "mp3", "m4a", or "wav"; best by default')
    postproc.add_option('--audio-quality', metavar='QUALITY', dest='audioquality', default='5',
            help='ffmpeg/avconv audio quality specification, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)')
    postproc.add_option('-k', '--keep-video', action='store_true', dest='keepvideo', default=False,
            help='keeps the video file on disk after the post-processing; the video is erased by default')
    postproc.add_option('--no-post-overwrites', action='store_true', dest='nopostoverwrites', default=False,
            help='do not overwrite post-processed files; the post-processed files are overwritten by default')


    parser.add_option_group(general)
    parser.add_option_group(selection)
    parser.add_option_group(filesystem)
    parser.add_option_group(verbosity)
    parser.add_option_group(video_format)
    parser.add_option_group(authentication)
    parser.add_option_group(postproc)

    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        userConf = os.path.join(xdg_config_home, 'youtube-dl.conf')
    else:
        userConf = os.path.join(os.path.expanduser('~'), '.config', 'youtube-dl.conf')
    argv = _readOptions('/etc/youtube-dl.conf') + _readOptions(userConf) + sys.argv[1:]
    opts, args = parser.parse_args(argv)

    return parser, opts, args

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**empty** &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.043**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.045**

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
	def _readOptions(filename_bytes):
		try:
			optionf = open(filename_bytes)
		except IOError:
			return [] # silently skip if file is not present
		try:
			res = []
			for l in optionf:
				res += shlex.split(l, comments=True)
		finally:
			optionf.close()
		return res

	def _format_option_string(option):
		''' ('-o', '--option') -> -o, --format METAVAR'''

		opts = []

		if option._short_opts: opts.append(option._short_opts[0])
		if option._long_opts: opts.append(option._long_opts[0])
		if len(opts) > 1: opts.insert(1, ', ')

		if option.takes_value(): opts.append(' %s' % option.metavar)

		return "".join(opts)

	def _find_term_columns():
		columns = os.environ.get('COLUMNS', None)
		if columns:
			return int(columns)

		try:
			sp = subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err = sp.communicate()
			return int(out.split()[1])
		except:
			pass
		return None

	max_width = 80
	max_help_position = 80

	# No need to wrap help messages if we're on a wide console
	columns = _find_term_columns()
	if columns: max_width = columns

	fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)
	fmt.format_option_strings = _format_option_string

	kw = {
		'version'   : __version__,
		'formatter' : fmt,
		'usage' : '%prog [options] url [url...]',
		'conflict_handler' : 'resolve',
	}

	parser = optparse.OptionParser(**kw)

	# option groups
	general        = optparse.OptionGroup(parser, 'General Options')
	selection      = optparse.OptionGroup(parser, 'Video Selection')
	authentication = optparse.OptionGroup(parser, 'Authentication Options')
	video_format   = optparse.OptionGroup(parser, 'Video Format Options')
	postproc       = optparse.OptionGroup(parser, 'Post-processing Options')
	filesystem     = optparse.OptionGroup(parser, 'Filesystem Options')
	verbosity      = optparse.OptionGroup(parser, 'Verbosity / Simulation Options')

	general.add_option('-h', '--help',
			action='help', help='print this help text and exit')
	general.add_option('-v', '--version',
			action='version', help='print program version and exit')
	general.add_option('-U', '--update',
			action='store_true', dest='update_self', help='update this program to latest version')
	general.add_option('-i', '--ignore-errors',
			action='store_true', dest='ignoreerrors', help='continue on download errors', default=False)
	general.add_option('-r', '--rate-limit',
			dest='ratelimit', metavar='LIMIT', help='download rate limit (e.g. 50k or 44.6m)')
	general.add_option('-R', '--retries',
			dest='retries', metavar='RETRIES', help='number of retries (default is %default)', default=10)
	general.add_option('--dump-user-agent',
			action='store_true', dest='dump_user_agent',
			help='display the current browser identification', default=False)
	general.add_option('--user-agent',
			dest='user_agent', help='specify a custom user agent', metavar='UA')
	general.add_option('--list-extractors',
			action='store_true', dest='list_extractors',
			help='List all supported extractors and the URLs they would handle', default=False)

	selection.add_option('--playlist-start',
			dest='playliststart', metavar='NUMBER', help='playlist video to start at (default is %default)', default=1)
	selection.add_option('--playlist-end',
			dest='playlistend', metavar='NUMBER', help='playlist video to end at (default is last)', default=-1)
	selection.add_option('--match-title', dest='matchtitle', metavar='REGEX',help='download only matching titles (regex or caseless sub-string)')
	selection.add_option('--reject-title', dest='rejecttitle', metavar='REGEX',help='skip download for matching titles (regex or caseless sub-string)')
	selection.add_option('--max-downloads', metavar='NUMBER', dest='max_downloads', help='Abort after downloading NUMBER files', default=None)

	authentication.add_option('-u', '--username',
			dest='username', metavar='USERNAME', help='account username')
	authentication.add_option('-p', '--password',
			dest='password', metavar='PASSWORD', help='account password')
	authentication.add_option('-n', '--netrc',
			action='store_true', dest='usenetrc', help='use .netrc authentication data', default=False)


	video_format.add_option('-f', '--format',
			action='store', dest='format', metavar='FORMAT', help='video format code')
	video_format.add_option('--all-formats',
			action='store_const', dest='format', help='download all available video formats', const='all')
	video_format.add_option('--prefer-free-formats',
			action='store_true', dest='prefer_free_formats', default=False, help='prefer free video formats unless a specific one is requested')
	video_format.add_option('--max-quality',
			action='store', dest='format_limit', metavar='FORMAT', help='highest quality format to download')
	video_format.add_option('-F', '--list-formats',
			action='store_true', dest='listformats', help='list all available formats (currently youtube only)')
	video_format.add_option('--write-srt',
			action='store_true', dest='writesubtitles',
			help='write video closed captions to a .srt file (currently youtube only)', default=False)
	video_format.add_option('--srt-lang',
			action='store', dest='subtitleslang', metavar='LANG',
			help='language of the closed captions to download (optional) use IETF language tags like \'en\'')


	verbosity.add_option('-q', '--quiet',
			action='store_true', dest='quiet', help='activates quiet mode', default=False)
	verbosity.add_option('-s', '--simulate',
			action='store_true', dest='simulate', help='do not download the video and do not write anything to disk', default=False)
	verbosity.add_option('--skip-download',
			action='store_true', dest='skip_download', help='do not download the video', default=False)
	verbosity.add_option('-g', '--get-url',
			action='store_true', dest='geturl', help='simulate, quiet but print URL', default=False)
	verbosity.add_option('-e', '--get-title',
			action='store_true', dest='gettitle', help='simulate, quiet but print title', default=False)
	verbosity.add_option('--get-thumbnail',
			action='store_true', dest='getthumbnail',
			help='simulate, quiet but print thumbnail URL', default=False)
	verbosity.add_option('--get-description',
			action='store_true', dest='getdescription',
			help='simulate, quiet but print video description', default=False)
	verbosity.add_option('--get-filename',
			action='store_true', dest='getfilename',
			help='simulate, quiet but print output filename', default=False)
	verbosity.add_option('--get-format',
			action='store_true', dest='getformat',
			help='simulate, quiet but print output format', default=False)
	verbosity.add_option('--no-progress',
			action='store_true', dest='noprogress', help='do not print progress bar', default=False)
	verbosity.add_option('--console-title',
			action='store_true', dest='consoletitle',
			help='display progress in console titlebar', default=False)
	verbosity.add_option('-v', '--verbose',
			action='store_true', dest='verbose', help='print various debugging information', default=False)


	filesystem.add_option('-t', '--title',
			action='store_true', dest='usetitle', help='use title in file name', default=False)
	filesystem.add_option('--id',
			action='store_true', dest='useid', help='use video ID in file name', default=False)
	filesystem.add_option('-l', '--literal',
			action='store_true', dest='useliteral', help='use literal title in file name', default=False)
	filesystem.add_option('-A', '--auto-number',
			action='store_true', dest='autonumber',
			help='number downloaded files starting from 00000', default=False)
	filesystem.add_option('-o', '--output',
			dest='outtmpl', metavar='TEMPLATE', help='output filename template. Use %(stitle)s to get the title, %(uploader)s for the uploader name, %(autonumber)s to get an automatically incremented number, %(ext)s for the filename extension, %(upload_date)s for the upload date (YYYYMMDD), %(extractor)s for the provider (youtube, metacafe, etc), %(id)s for the video id and %% for a literal percent. Use - to output to stdout.')
	filesystem.add_option('-a', '--batch-file',
			dest='batchfile', metavar='FILE', help='file containing URLs to download (\'-\' for stdin)')
	filesystem.add_option('-w', '--no-overwrites',
			action='store_true', dest='nooverwrites', help='do not overwrite files', default=False)
	filesystem.add_option('-c', '--continue',
			action='store_true', dest='continue_dl', help='resume partially downloaded files', default=True)
	filesystem.add_option('--no-continue',
			action='store_false', dest='continue_dl',
			help='do not resume partially downloaded files (restart from beginning)')
	filesystem.add_option('--cookies',
			dest='cookiefile', metavar='FILE', help='file to read cookies from and dump cookie jar in')
	filesystem.add_option('--no-part',
			action='store_true', dest='nopart', help='do not use .part files', default=False)
	filesystem.add_option('--no-mtime',
			action='store_false', dest='updatetime',
			help='do not use the Last-modified header to set the file modification time', default=True)
	filesystem.add_option('--write-description',
			action='store_true', dest='writedescription',
			help='write video description to a .description file', default=False)
	filesystem.add_option('--write-info-json',
			action='store_true', dest='writeinfojson',
			help='write video metadata to a .info.json file', default=False)


	postproc.add_option('-x', '--extract-audio', action='store_true', dest='extractaudio', default=False,
			help='convert video files to audio-only files (requires ffmpeg or avconv and ffprobe or avprobe)')
	postproc.add_option('--audio-format', metavar='FORMAT', dest='audioformat', default='best',
			help='"best", "aac", "vorbis", "mp3", "m4a", or "wav"; best by default')
	postproc.add_option('--audio-quality', metavar='QUALITY', dest='audioquality', default='5',
			help='ffmpeg/avconv audio quality specification, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)')
	postproc.add_option('-k', '--keep-video', action='store_true', dest='keepvideo', default=False,
			help='keeps the video file on disk after the post-processing; the video is erased by default')


	parser.add_option_group(general)
	parser.add_option_group(selection)
	parser.add_option_group(filesystem)
	parser.add_option_group(verbosity)
	parser.add_option_group(video_format)
	parser.add_option_group(authentication)
	parser.add_option_group(postproc)

	xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
	if xdg_config_home:
		userConf = os.path.join(xdg_config_home, 'youtube-dl.conf')
	else:
		userConf = os.path.join(os.path.expanduser('~'), '.config', 'youtube-dl.conf')
	argv = _readOptions('/etc/youtube-dl.conf') + _readOptions(userConf) + sys.argv[1:]
	opts, args = parser.parse_args(argv)

	return parser, opts, args

def gen_extractors():
	""" Return a list of an instance of every supported extractor.
	The order does matter; the first extractor matched is the one handling the URL.
	"""
	return [
		YoutubePlaylistIE(),
		YoutubeChannelIE(),
		YoutubeUserIE(),
		YoutubeSearchIE(),
		YoutubeIE(),
		MetacafeIE(),
		DailymotionIE(),
		GoogleIE(),
		GoogleSearchIE(),
		PhotobucketIE(),
		YahooIE(),
		YahooSearchIE(),
		DepositFilesIE(),
		FacebookIE(),
		BlipTVUserIE(),
		BlipTVIE(),
		VimeoIE(),
		MyVideoIE(),
		ComedyCentralIE(),
		EscapistIE(),
		CollegeHumorIE(),
		XVideosIE(),
		SoundcloudIE(),
		InfoQIE(),
		MixcloudIE(),
		StanfordOpenClassroomIE(),
		MTVIE(),
		YoukuIE(),
		XNXXIE(),
		GooglePlusIE(),
<<<<<<< a
		PornotubeIE(),
		YouPornIE(),
		YouJizzIE(),
=======

>>>>>>> b
		GenericIE()
	]

```

</td>
<td valign="top">

```python

```

</td>
<td valign="top">

```python

```

</td>
<td valign="top">

```python

```

</td>
<td valign="top">

```python
    def _readOptions(filename_bytes):
        try:
            optionf = open(filename_bytes)
        except IOError:
            return [] # silently skip if file is not present
        try:
            res = []
            for l in optionf:
                res += shlex.split(l, comments=True)
        finally:
            optionf.close()
        return res

    def _format_option_string(option):
        ''' ('-o', '--option') -> -o, --format METAVAR'''

        opts = []

        if option._short_opts:
            opts.append(option._short_opts[0])
        if option._long_opts:
            opts.append(option._long_opts[0])
        if len(opts) > 1:
            opts.insert(1, ', ')

        if option.takes_value(): opts.append(' %s' % option.metavar)

        return "".join(opts)

    def _find_term_columns():
        columns = os.environ.get('COLUMNS', None)
        if columns:
            return int(columns)

        try:
            sp = subprocess.Popen(['stty', 'size'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = sp.communicate()
            return int(out.split()[1])
        except:
            pass
        return None

    max_width = 80
    max_help_position = 80

    # No need to wrap help messages if we're on a wide console
    columns = _find_term_columns()
    if columns: max_width = columns

    fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)
    fmt.format_option_strings = _format_option_string

    kw = {
        'version'   : __version__,
        'formatter' : fmt,
        'usage' : '%prog [options] url [url...]',
        'conflict_handler' : 'resolve',
    }

    parser = optparse.OptionParser(**kw)

    # option groups
    general        = optparse.OptionGroup(parser, 'General Options')
    selection      = optparse.OptionGroup(parser, 'Video Selection')
    authentication = optparse.OptionGroup(parser, 'Authentication Options')
    video_format   = optparse.OptionGroup(parser, 'Video Format Options')
    postproc       = optparse.OptionGroup(parser, 'Post-processing Options')
    filesystem     = optparse.OptionGroup(parser, 'Filesystem Options')
    verbosity      = optparse.OptionGroup(parser, 'Verbosity / Simulation Options')

    general.add_option('-h', '--help',
            action='help', help='print this help text and exit')
    general.add_option('-v', '--version',
            action='version', help='print program version and exit')
    general.add_option('-U', '--update',
            action='store_true', dest='update_self', help='update this program to latest version')
    general.add_option('-i', '--ignore-errors',
            action='store_true', dest='ignoreerrors', help='continue on download errors', default=False)
    general.add_option('-r', '--rate-limit',
            dest='ratelimit', metavar='LIMIT', help='download rate limit (e.g. 50k or 44.6m)')
    general.add_option('-R', '--retries',
            dest='retries', metavar='RETRIES', help='number of retries (default is %default)', default=10)
    general.add_option('--buffer-size',
            dest='buffersize', metavar='SIZE', help='size of download buffer (e.g. 1024 or 16k) (default is %default)', default="1024")
    general.add_option('--no-resize-buffer',
            action='store_true', dest='noresizebuffer',
            help='do not automatically adjust the buffer size. By default, the buffer size is automatically resized from an initial value of SIZE.', default=False)
    general.add_option('--dump-user-agent',
            action='store_true', dest='dump_user_agent',
            help='display the current browser identification', default=False)
    general.add_option('--user-agent',
            dest='user_agent', help='specify a custom user agent', metavar='UA')
    general.add_option('--list-extractors',
            action='store_true', dest='list_extractors',
            help='List all supported extractors and the URLs they would handle', default=False)
    general.add_option('--test', action='store_true', dest='test', default=False, help=optparse.SUPPRESS_HELP)

    selection.add_option('--playlist-start',
            dest='playliststart', metavar='NUMBER', help='playlist video to start at (default is %default)', default=1)
    selection.add_option('--playlist-end',
            dest='playlistend', metavar='NUMBER', help='playlist video to end at (default is last)', default=-1)
    selection.add_option('--match-title', dest='matchtitle', metavar='REGEX',help='download only matching titles (regex or caseless sub-string)')
    selection.add_option('--reject-title', dest='rejecttitle', metavar='REGEX',help='skip download for matching titles (regex or caseless sub-string)')
    selection.add_option('--max-downloads', metavar='NUMBER', dest='max_downloads', help='Abort after downloading NUMBER files', default=None)

    authentication.add_option('-u', '--username',
            dest='username', metavar='USERNAME', help='account username')
    authentication.add_option('-p', '--password',
            dest='password', metavar='PASSWORD', help='account password')
    authentication.add_option('-n', '--netrc',
            action='store_true', dest='usenetrc', help='use .netrc authentication data', default=False)


    video_format.add_option('-f', '--format',
            action='store', dest='format', metavar='FORMAT', help='video format code')
    video_format.add_option('--all-formats',
            action='store_const', dest='format', help='download all available video formats', const='all')
    video_format.add_option('--prefer-free-formats',
            action='store_true', dest='prefer_free_formats', default=False, help='prefer free video formats unless a specific one is requested')
    video_format.add_option('--max-quality',
            action='store', dest='format_limit', metavar='FORMAT', help='highest quality format to download')
    video_format.add_option('-F', '--list-formats',
            action='store_true', dest='listformats', help='list all available formats (currently youtube only)')
    video_format.add_option('--write-srt',
            action='store_true', dest='writesubtitles',
            help='write video closed captions to a .srt file (currently youtube only)', default=False)
    video_format.add_option('--srt-lang',
            action='store', dest='subtitleslang', metavar='LANG',
            help='language of the closed captions to download (optional) use IETF language tags like \'en\'')


    verbosity.add_option('-q', '--quiet',
            action='store_true', dest='quiet', help='activates quiet mode', default=False)
    verbosity.add_option('-s', '--simulate',
            action='store_true', dest='simulate', help='do not download the video and do not write anything to disk', default=False)
    verbosity.add_option('--skip-download',
            action='store_true', dest='skip_download', help='do not download the video', default=False)
    verbosity.add_option('-g', '--get-url',
            action='store_true', dest='geturl', help='simulate, quiet but print URL', default=False)
    verbosity.add_option('-e', '--get-title',
            action='store_true', dest='gettitle', help='simulate, quiet but print title', default=False)
    verbosity.add_option('--get-thumbnail',
            action='store_true', dest='getthumbnail',
            help='simulate, quiet but print thumbnail URL', default=False)
    verbosity.add_option('--get-description',
            action='store_true', dest='getdescription',
            help='simulate, quiet but print video description', default=False)
    verbosity.add_option('--get-filename',
            action='store_true', dest='getfilename',
            help='simulate, quiet but print output filename', default=False)
    verbosity.add_option('--get-format',
            action='store_true', dest='getformat',
            help='simulate, quiet but print output format', default=False)
    verbosity.add_option('--no-progress',
            action='store_true', dest='noprogress', help='do not print progress bar', default=False)
    verbosity.add_option('--console-title',
            action='store_true', dest='consoletitle',
            help='display progress in console titlebar', default=False)
    verbosity.add_option('-v', '--verbose',
            action='store_true', dest='verbose', help='print various debugging information', default=False)


    filesystem.add_option('-t', '--title',
            action='store_true', dest='usetitle', help='use title in file name', default=False)
    filesystem.add_option('--id',
            action='store_true', dest='useid', help='use video ID in file name', default=False)
    filesystem.add_option('-l', '--literal',
            action='store_true', dest='usetitle', help='[deprecated] alias of --title', default=False)
    filesystem.add_option('-A', '--auto-number',
            action='store_true', dest='autonumber',
            help='number downloaded files starting from 00000', default=False)
    filesystem.add_option('-o', '--output',
            dest='outtmpl', metavar='TEMPLATE', help='output filename template. Use %(title)s to get the title, %(uploader)s for the uploader name, %(uploader_id)s for the uploader nickname if different, %(autonumber)s to get an automatically incremented number, %(ext)s for the filename extension, %(upload_date)s for the upload date (YYYYMMDD), %(extractor)s for the provider (youtube, metacafe, etc), %(id)s for the video id and %% for a literal percent. Use - to output to stdout. Can also be used to download to a different directory, for example with -o \'/my/downloads/%(uploader)s/%(title)s-%(id)s.%(ext)s\' .')
    filesystem.add_option('--restrict-filenames',
            action='store_true', dest='restrictfilenames',
            help='Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames', default=False)
    filesystem.add_option('-a', '--batch-file',
            dest='batchfile', metavar='FILE', help='file containing URLs to download (\'-\' for stdin)')
    filesystem.add_option('-w', '--no-overwrites',
            action='store_true', dest='nooverwrites', help='do not overwrite files', default=False)
    filesystem.add_option('-c', '--continue',
            action='store_true', dest='continue_dl', help='resume partially downloaded files', default=True)
    filesystem.add_option('--no-continue',
            action='store_false', dest='continue_dl',
            help='do not resume partially downloaded files (restart from beginning)')
    filesystem.add_option('--cookies',
            dest='cookiefile', metavar='FILE', help='file to read cookies from and dump cookie jar in')
    filesystem.add_option('--no-part',
            action='store_true', dest='nopart', help='do not use .part files', default=False)
    filesystem.add_option('--no-mtime',
            action='store_false', dest='updatetime',
            help='do not use the Last-modified header to set the file modification time', default=True)
    filesystem.add_option('--write-description',
            action='store_true', dest='writedescription',
            help='write video description to a .description file', default=False)
    filesystem.add_option('--write-info-json',
            action='store_true', dest='writeinfojson',
            help='write video metadata to a .info.json file', default=False)


    postproc.add_option('-x', '--extract-audio', action='store_true', dest='extractaudio', default=False,
            help='convert video files to audio-only files (requires ffmpeg or avconv and ffprobe or avprobe)')
    postproc.add_option('--audio-format', metavar='FORMAT', dest='audioformat', default='best',
            help='"best", "aac", "vorbis", "mp3", "m4a", or "wav"; best by default')
    postproc.add_option('--audio-quality', metavar='QUALITY', dest='audioquality', default='5',
            help='ffmpeg/avconv audio quality specification, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)')
    postproc.add_option('-k', '--keep-video', action='store_true', dest='keepvideo', default=False,
            help='keeps the video file on disk after the post-processing; the video is erased by default')
    postproc.add_option('--no-post-overwrites', action='store_true', dest='nopostoverwrites', default=False,
            help='do not overwrite post-processed files; the post-processed files are overwritten by default')


    parser.add_option_group(general)
    parser.add_option_group(selection)
    parser.add_option_group(filesystem)
    parser.add_option_group(verbosity)
    parser.add_option_group(video_format)
    parser.add_option_group(authentication)
    parser.add_option_group(postproc)

    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        userConf = os.path.join(xdg_config_home, 'youtube-dl.conf')
    else:
        userConf = os.path.join(os.path.expanduser('~'), '.config', 'youtube-dl.conf')
    argv = _readOptions('/etc/youtube-dl.conf') + _readOptions(userConf) + sys.argv[1:]
    opts, args = parser.parse_args(argv)

    return parser, opts, args

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**empty** &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**empty** &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**empty** &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
