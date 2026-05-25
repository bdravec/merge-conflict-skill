# `text` bucket — worked examples

Changes in **textual content** — docstrings, comments, string literals. Not code logic.

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0x69c45106c1328782`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.932)</th>
<th align="left">v2-sys (max=0.673)</th>
<th align="left">v2.1-sys (max=0.999)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        filters: int, the dimension of the output space (the number of filters
            in the convolution).
        kernel_size: int or tuple/list of 2 integer, specifying the size of the
            convolution window.
        strides: int or tuple/list of 2 integer, specifying the stride length
            of the convolution. `strides > 1` is incompatible with
            `dilation_rate > 1`.
        padding: string, either `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding evenly to
            the left/right or up/down of the input such that output has the same
            height/width dimension as the input.
        data_format: string, either `"channels_last"` or `"channels_first"`.
            The ordering of the dimensions in the inputs. `"channels_last"`
            corresponds to inputs with shape
            `(batch_size, channels, height, width)`
            while `"channels_first"` corresponds to inputs with shape
            `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `"channels_last"`.
        dilation_rate: int or tuple/list of 2 integers, specifying the dilation
            rate to use for dilated convolution.
        groups: A positive int specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters // groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis.
            Input channels and `filters` must both be divisible by `groups`.
        activation: Activation function. If `None`, no activation is applied.
        use_bias: bool, if `True`, bias will be added to the output.
        kernel_initializer: Initializer for the convolution kernel. If `None`,
            the default initializer (`"glorot_uniform"`) will be used.
        bias_initializer: Initializer for the bias vector. If `None`, the
            default initializer (`"zeros"`) will be used.
        kernel_regularizer: Optional regularizer for the convolution kernel.
        bias_regularizer: Optional regularizer for the bias vector.
        activity_regularizer: Optional regularizer function for the output.
        kernel_constraint: Optional projection function to be applied to the
            kernel after being updated by an `Optimizer` (e.g. used to implement
            norm constraints or value constraints for layer weights). The
            function must take as input the unprojected variable and must return
            the projected variable (which must have the same shape). Constraints
            are not safe to use when doing asynchronous distributed training.
        bias_constraint: Optional projection function to be applied to the
            bias after being updated by an `Optimizer`.
=======
      filters: Integer, the dimensionality of the output space (i.e. the number
        of output filters in the convolution).
      kernel_size: An integer or tuple/list of 2 integers, specifying the height
        and width of the 2D convolution window. Can be a single integer to
        specify the same value for all spatial dimensions.
      strides: An integer or tuple/list of 2 integers, specifying the strides of
        the convolution along the height and width. Can be a single integer to
        specify the same value for all spatial dimensions. Specifying any stride
        value != 1 is incompatible with specifying any `dilation_rate` value !=
        1.
      padding: one of `"valid"` or `"same"` (case-insensitive).
        `"valid"` means no padding. `"same"` results in padding with zeros
        evenly to the left/right or up/down of the input. When `padding="same"`
        and `strides=1`, the output has the same size as the input.
      data_format: A string, one of `channels_last` (default) or
        `channels_first`.  The ordering of the dimensions in the inputs.
        `channels_last` corresponds to inputs with shape `(batch_size, height,
        width, channels)` while `channels_first` corresponds to inputs with
        shape `(batch_size, channels, height, width)`. It defaults to the
        `image_data_format` value found in your Keras config file at
        `~/.keras/keras.json`. If you never set it, then it will be
        `channels_last`. Note that the `channels_first` format is currently not
        supported by TensorFlow on CPU.
      dilation_rate: an integer or tuple/list of 2 integers, specifying the
        dilation rate to use for dilated convolution. Can be a single integer to
        specify the same value for all spatial dimensions. Currently, specifying
        any `dilation_rate` value != 1 is incompatible with specifying any
        stride value != 1.
      groups: A positive integer specifying the number of groups in which the
        input is split along the channel axis. Each group is convolved
        separately with `filters / groups` filters. The output is the
        concatenation of all the `groups` results along the channel axis. Input
        channels and `filters` must both be divisible by `groups`.
      activation: Activation function to use. If you don't specify anything, no
        activation is applied (see `keras.activations`).
      use_bias: Boolean, whether the layer uses a bias vector.
      kernel_initializer: Initializer for the `kernel` weights matrix (see
        `keras.initializers`). Defaults to 'glorot_uniform'.
      bias_initializer: Initializer for the bias vector (see
        `keras.initializers`). Defaults to 'zeros'.
      kernel_regularizer: Regularizer function applied to the `kernel` weights
        matrix (see `keras.regularizers`).
      bias_regularizer: Regularizer function applied to the bias vector (see
        `keras.regularizers`).
      activity_regularizer: Regularizer function applied to the output of the
        layer (its "activation") (see `keras.regularizers`).
      kernel_constraint: Constraint function applied to the kernel matrix (see
        `keras.constraints`).
      bias_constraint: Constraint function applied to the bias vector (see
        `keras.constraints`).
>>>>>>> b

```

</td>
<td valign="top">

```python
outputs. If `use_bias` is True, a bias vector is created and added to the
    outputs. Finally, if `activation` is not `None`, it is applied to the
    outputs as well.

    Args:
        filters: int, the dimension of the output space (the number of filters
            in the convolution).
        kernel_size: int or tuple/list of 2 integer, specifying the size of the
            convolution window.
        strides: int or tuple/list of 2 integer, specifying the stride length
            of the convolution. `strides > 1` is incompatible with
            `dilation_rate > 1`.
        padding: string, either `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding evenly to
            the left/right or up/down of the input such that output has the same
            height/width dimension as the input.
        data_format: string, either `"channels_last"` or `"channels_first"`.
            The ordering of the dimensions in the inputs. `"channels_last"`
            corresponds to inputs with shape
            `(batch_size, channels, height, width)`
            while `"channels_first"` corresponds to inputs with shape
            `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `"channels_last"`.
        dilation_rate: int or tuple/list of 2 integers, specifying the dilation
            rate to use for dilated convolution.
        groups: A positive int specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters // groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis.
            Input channels and `filters` must both be divisible by `groups`.
        activation: Activation function. If `None`, no activation is applied.
        use_bias: bool, if `True`, bias will be added to the output.
        kernel_initializer: Initializer for the convolution kernel. If `None`,
            the default initializer (`"glorot_uniform"`) will be used.
        bias_initializer: Initializer for the bias vector. If `None`, the
            default initializer (`"zeros"`) will be used.
        kernel_regularizer: Optional regularizer for the convolution kernel.
        bias_regularizer: Optional regularizer for the bias vector.
        activity_regularizer: Optional regularizer function for the output.
        kernel_constraint: Optional projection function to be applied to the
            kernel after being updated by an `Optimizer` (e.g. used to implement
            norm constraints or value constraints for layer weights). The
            function must take as input the unprojected variable and must return
            the projected variable (which must have the same shape). Constraints
            are not safe to use when doing asynchronous distributed training.
        bias_constraint: Optional projection function to be applied to the
            bias after being updated by an `Optimizer`.

    Input shape:
    - If `data_format="channels_last"`:
        A 4D tensor with shape: `(batch_size, height, width, channels)`
    - If `data_format="channels_first"`:
        A 4D tensor with shape: `(batch_size, channels, height, width)`

    Output shape:
    - If `data_format="channels_last"`:
        A 4D tensor with shape: `(batch_size, filters, height, width)`
    - If `data_format="channels_first"`:
        A 4D tensor with shape: `(batch_size, height, width, filters)`

    Note: The `strides` value affects the output shape (which is a reduction
    factor), while `dilation_rate` affects the receptive field. `strides > 1`
    and `dilation_rate > 1` are incompatible.
```

</td>
<td valign="top">

```python
filters: Integer, the dimensionality of the output space (i.e. the number
        of output filters in the convolution).
    kernel_size: An integer or tuple/list of 2 integers, specifying the height
        and width of the 2D convolution window. Can be a single integer to
        specify the same value for all spatial dimensions.
    strides: An integer or tuple/list of 2 integers, specifying the strides of
        the convolution along the height and width. Can be a single integer to
        specify the same value for all spatial dimensions. Specifying any stride
        value != 1 is incompatible with specifying any `dilation_rate` value !=
        1.
    padding: one of `"valid"` or `"same"` (case-insensitive).
        `"valid"` means no padding. `"same"` results in padding with zeros
        evenly to the left/right or up/down of the input. When `padding="same"`
        and `strides=1`, the output has the same size as the input.
    data_format: A string, one of `channels_last` (default) or
        `channels_first`.  The ordering of the dimensions in the inputs.
        `channels_last` corresponds to inputs with shape `(batch_size, height,
        width, channels)` while `channels_first` corresponds to inputs with
        shape `(batch_size, channels, height, width)`. It defaults to the
        `image_data_format` value found in your Keras config file at
        `~/.keras/keras.json`. If you never set it, then it will be
        `channels_last`. Note that the `channels_first` format is currently not
        supported by TensorFlow on CPU.
    dilation_rate: an integer or tuple/list of 2 integers, specifying the
        dilation rate to use for dilated convolution. Can be a single integer to
        specify the same value for all spatial dimensions. Currently, specifying
        any `dilation_rate` value != 1 is incompatible with specifying any
        stride value != 1.
    groups: A positive integer specifying the number of groups in which the
        input is split along the channel axis. Each group is convolved
        separately with `filters / groups` filters. The output is the
        concatenation of all the `groups` results along the channel axis. Input
        channels and `filters` must both be divisible by `groups`.
    activation: Activation function to use. If you don't specify anything, no
        activation is applied (see `keras.activations`).
    use_bias: Boolean, whether the layer uses a bias vector.
    kernel_initializer: Initializer for the `kernel` weights matrix (see
        `keras.initializers`). Defaults to 'glorot_uniform'.
    bias_initializer: Initializer for the bias vector (see
        `keras.initializers`). Defaults to 'zeros'.
    kernel_regularizer: Regularizer function applied to the `kernel` weights
        matrix (see `keras.regularizers`).
    bias_regularizer: Regularizer function applied to the bias vector (see
        `keras.regularizers`).
    activity_regularizer: Regularizer function applied to the output of the
        layer (its "activation") (see `keras.regularizers`).
    kernel_constraint: Constraint function applied to the kernel matrix (see
        `keras.constraints`).
    bias_constraint: Constraint function applied to the bias vector (see
        `keras.constraints`).
```

</td>
<td valign="top">

```python
filters: int, the dimension of the output space (the number of filters
        in the convolution).
    kernel_size: int or tuple/list of 2 integer, specifying the size of the
        convolution window.
    strides: int or tuple/list of 2 integer, specifying the stride length
        of the convolution. `strides > 1` is incompatible with
        `dilation_rate > 1`.
    padding: string, either `"valid"` or `"same"` (case-insensitive).
        `"valid"` means no padding. `"same"` results in padding evenly to
        the left/right or up/down of the input such that output has the same
        height/width dimension as the input.
    data_format: string, either `"channels_last"` or `"channels_first"`.
        The ordering of the dimensions in the inputs. `"channels_last"`
        corresponds to inputs with shape
        `(batch_size, channels, height, width)`
        while `"channels_first"` corresponds to inputs with shape
        `(batch_size, channels, height, width)`. It defaults to the
        `image_data_format` value found in your Keras config file at
        `~/.keras/keras.json`. If you never set it, then it will be
        `"channels_last"`.
    dilation_rate: int or tuple/list of 2 integers, specifying the dilation
        rate to use for dilated convolution.
    groups: A positive int specifying the number of groups in which the
        input is split along the channel axis. Each group is convolved
        separately with `filters // groups` filters. The output is the
        concatenation of all the `groups` results along the channel axis.
        Input channels and `filters` must both be divisible by `groups`.
    activation: Activation function. If `None`, no activation is applied.
    use_bias: bool, if `True`, bias will be added to the output.
    kernel_initializer: Initializer for the convolution kernel. If `None`,
        the default initializer (`"glorot_uniform"`) will be used.
    bias_initializer: Initializer for the bias vector. If `None`, the
        default initializer (`"zeros"`) will be used.
    kernel_regularizer: Optional regularizer for the convolution kernel.
    bias_regularizer: Optional regularizer for the bias vector.
    activity_regularizer: Optional regularizer function for the output.
    kernel_constraint: Optional projection function to be applied to the
        kernel after being updated by an `Optimizer` (e.g. used to implement
        norm constraints or value constraints for layer weights). The
        function must take as input the unprojected variable and must return
        the projected variable (which must have the same shape). Constraints
        are not safe to use when doing asynchronous distributed training.
    bias_constraint: Optional projection function to be applied to the
        bias after being updated by an `Optimizer`.
```

</td>
<td valign="top">

```python
    Args:
        filters: int, the dimension of the output space (the number of filters
            in the convolution).
        kernel_size: int or tuple/list of 2 integer, specifying the size of the
            convolution window.
        strides: int or tuple/list of 2 integer, specifying the stride length
            of the convolution. `strides > 1` is incompatible with
            `dilation_rate > 1`.
        padding: string, either `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding evenly to
            the left/right or up/down of the input such that output has the same
            height/width dimension as the input.
        data_format: string, either `"channels_last"` or `"channels_first"`.
            The ordering of the dimensions in the inputs. `"channels_last"`
            corresponds to inputs with shape
            `(batch_size, channels, height, width)`
            while `"channels_first"` corresponds to inputs with shape
            `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `"channels_last"`.
        dilation_rate: int or tuple/list of 2 integers, specifying the dilation
            rate to use for dilated convolution.
        groups: A positive int specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters // groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis.
            Input channels and `filters` must both be divisible by `groups`.
        activation: Activation function. If `None`, no activation is applied.
        use_bias: bool, if `True`, bias will be added to the output.
        kernel_initializer: Initializer for the convolution kernel. If `None`,
            the default initializer (`"glorot_uniform"`) will be used.
        bias_initializer: Initializer for the bias vector. If `None`, the
            default initializer (`"zeros"`) will be used.
        kernel_regularizer: Optional regularizer for the convolution kernel.
        bias_regularizer: Optional regularizer for the bias vector.
        activity_regularizer: Optional regularizer function for the output.
        kernel_constraint: Optional projection function to be applied to the
            kernel after being updated by an `Optimizer` (e.g. used to implement
            norm constraints or value constraints for layer weights). The
            function must take as input the unprojected variable and must return
            the projected variable (which must have the same shape). Constraints
            are not safe to use when doing asynchronous distributed training.
        bias_constraint: Optional projection function to be applied to the
            bias after being updated by an `Optimizer`.
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.932**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.673**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.999**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.667)</th>
<th align="left">v2-sys (max=0.667)</th>
<th align="left">v2.1-sys (max=0.672)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        filters: int, the dimension of the output space (the number of filters
            in the convolution).
        kernel_size: int or tuple/list of 2 integer, specifying the size of the
            convolution window.
        strides: int or tuple/list of 2 integer, specifying the stride length
            of the convolution. `strides > 1` is incompatible with
            `dilation_rate > 1`.
        padding: string, either `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding evenly to
            the left/right or up/down of the input such that output has the same
            height/width dimension as the input.
        data_format: string, either `"channels_last"` or `"channels_first"`.
            The ordering of the dimensions in the inputs. `"channels_last"`
            corresponds to inputs with shape
            `(batch_size, channels, height, width)`
            while `"channels_first"` corresponds to inputs with shape
            `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `"channels_last"`.
        dilation_rate: int or tuple/list of 2 integers, specifying the dilation
            rate to use for dilated convolution.
        groups: A positive int specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters // groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis.
            Input channels and `filters` must both be divisible by `groups`.
        activation: Activation function. If `None`, no activation is applied.
        use_bias: bool, if `True`, bias will be added to the output.
        kernel_initializer: Initializer for the convolution kernel. If `None`,
            the default initializer (`"glorot_uniform"`) will be used.
        bias_initializer: Initializer for the bias vector. If `None`, the
            default initializer (`"zeros"`) will be used.
        kernel_regularizer: Optional regularizer for the convolution kernel.
        bias_regularizer: Optional regularizer for the bias vector.
        activity_regularizer: Optional regularizer function for the output.
        kernel_constraint: Optional projection function to be applied to the
            kernel after being updated by an `Optimizer` (e.g. used to implement
            norm constraints or value constraints for layer weights). The
            function must take as input the unprojected variable and must return
            the projected variable (which must have the same shape). Constraints
            are not safe to use when doing asynchronous distributed training.
        bias_constraint: Optional projection function to be applied to the
            bias after being updated by an `Optimizer`.
=======
      filters: Integer, the dimensionality of the output space (i.e. the number
        of output filters in the convolution).
      kernel_size: An integer or tuple/list of 2 integers, specifying the height
        and width of the 2D convolution window. Can be a single integer to
        specify the same value for all spatial dimensions.
      strides: An integer or tuple/list of 2 integers, specifying the strides of
        the convolution along the height and width. Can be a single integer to
        specify the same value for all spatial dimensions. Specifying any stride
        value != 1 is incompatible with specifying any `dilation_rate` value !=
        1.
      padding: one of `"valid"` or `"same"` (case-insensitive).
        `"valid"` means no padding. `"same"` results in padding with zeros
        evenly to the left/right or up/down of the input. When `padding="same"`
        and `strides=1`, the output has the same size as the input.
      data_format: A string, one of `channels_last` (default) or
        `channels_first`.  The ordering of the dimensions in the inputs.
        `channels_last` corresponds to inputs with shape `(batch_size, height,
        width, channels)` while `channels_first` corresponds to inputs with
        shape `(batch_size, channels, height, width)`. It defaults to the
        `image_data_format` value found in your Keras config file at
        `~/.keras/keras.json`. If you never set it, then it will be
        `channels_last`. Note that the `channels_first` format is currently not
        supported by TensorFlow on CPU.
      dilation_rate: an integer or tuple/list of 2 integers, specifying the
        dilation rate to use for dilated convolution. Can be a single integer to
        specify the same value for all spatial dimensions. Currently, specifying
        any `dilation_rate` value != 1 is incompatible with specifying any
        stride value != 1.
      groups: A positive integer specifying the number of groups in which the
        input is split along the channel axis. Each group is convolved
        separately with `filters / groups` filters. The output is the
        concatenation of all the `groups` results along the channel axis. Input
        channels and `filters` must both be divisible by `groups`.
      activation: Activation function to use. If you don't specify anything, no
        activation is applied (see `keras.activations`).
      use_bias: Boolean, whether the layer uses a bias vector.
      kernel_initializer: Initializer for the `kernel` weights matrix (see
        `keras.initializers`). Defaults to 'glorot_uniform'.
      bias_initializer: Initializer for the bias vector (see
        `keras.initializers`). Defaults to 'zeros'.
      kernel_regularizer: Regularizer function applied to the `kernel` weights
        matrix (see `keras.regularizers`).
      bias_regularizer: Regularizer function applied to the bias vector (see
        `keras.regularizers`).
      activity_regularizer: Regularizer function applied to the output of the
        layer (its "activation") (see `keras.regularizers`).
      kernel_constraint: Constraint function applied to the kernel matrix (see
        `keras.constraints`).
      bias_constraint: Constraint function applied to the bias vector (see
        `keras.constraints`).
>>>>>>> b

```

</td>
<td valign="top">

```python
outputs. If `use_bias` is True, a bias vector is created and added to the
    outputs. Finally, if `activation` is not `None`, it is applied to the
    outputs as well.

    Args:
        filters: Integer, the dimensionality of the output space (i.e. the number
            of output filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the height
            and width of the 2D convolution window. Can be a single integer to
            specify the same value for all spatial dimensions.
        strides: An integer or tuple/list of 2 integers, specifying the strides of
            the convolution along the height and width. Can be a single integer to
            specify the same value for all spatial dimensions. Specifying any stride
            value != 1 is incompatible with specifying any `dilation_rate` value !=
            1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding with zeros
            evenly to the left/right or up/down of the input. When `padding="same"`
            and `strides=1`, the output has the same size as the input.
        data_format: A string, one of `channels_last` (default) or
            `channels_first`. The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape `(batch_size, height,
            width, channels)` while `channels_first` corresponds to inputs with
            shape `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `channels_last`. Note that the `channels_first` format is currently not
            supported by TensorFlow on CPU.
        dilation_rate: an integer or tuple/list of 2 integers, specifying the
            dilation rate to use for dilated convolution. Can be a single integer to
            specify the same value for all spatial dimensions. Currently, specifying
            any `dilation_rate` value != 1 is incompatible with specifying any
            stride value != 1.
        groups: A positive integer specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters / groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis. Input
            channels and `filters` must both be divisible by `groups`.
        activation: Activation function to use. If you don't specify anything, no
            activation is applied (see `keras.activations`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix (see
            `keras.initializers`). Defaults to 'glorot_uniform'.
        bias_initializer: Initializer for the bias vector (see
            `keras.initializers`). Defaults to 'zeros'.
        kernel_regularizer: Regularizer function applied to the `kernel` weights
            matrix (see `keras.regularizers`).
        bias_regularizer: Regularizer function applied to the bias vector (see
            `keras.regularizers`).
        activity_regularizer: Regularizer function applied to the output of the
            layer (its "activation") (see `keras.regularizers`).
        kernel_constraint: Constraint function applied to the kernel matrix (see
            `keras.constraints`).
        bias_constraint: Constraint function applied to the bias vector (see
            `keras.constraints`).

    Input shape:
    - If `data_format="channels_last"`:
        A 4D tensor with shape: `(batch_size, height, width, channels)`
    - If `data_format="channels_first"`:
        A 4D tensor with shape: `(batch_size, channels, height, width)`
```

</td>
<td valign="top">

```python
outputs. If `use_bias` is True, a bias vector is created and added to the
    outputs. Finally, if `activation` is not `None`, it is applied to the
    outputs as well.

    Args:
        filters: Integer, the dimensionality of the output space (i.e. the number
          of output filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the height
          and width of the 2D convolution window. Can be a single integer to
          specify the same value for all spatial dimensions.
        strides: An integer or tuple/list of 2 integers, specifying the strides of
          the convolution along the height and width. Can be a single integer to
          specify the same value for all spatial dimensions. Specifying any stride
          value != 1 is incompatible with specifying any `dilation_rate` value !=
          1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
          `"valid"` means no padding. `"same"` results in padding with zeros
          evenly to the left/right or up/down of the input. When `padding="same"`
          and `strides=1`, the output has the same size as the input.
        data_format: A string, one of `channels_last` (default) or
          `channels_first`.  The ordering of the dimensions in the inputs.
          `channels_last` corresponds to inputs with shape `(batch_size, height,
          width, channels)` while `channels_first` corresponds to inputs with
          shape `(batch_size, channels, height, width)`. It defaults to the
          `image_data_format` value found in your Keras config file at
          `~/.keras/keras.json`. If you never set it, then it will be
          `channels_last`. Note that the `channels_first` format is currently not
          supported by TensorFlow on CPU.
        dilation_rate: an integer or tuple/list of 2 integers, specifying the
          dilation rate to use for dilated convolution. Can be a single integer to
          specify the same value for all spatial dimensions. Currently, specifying
          any `dilation_rate` value != 1 is incompatible with specifying any
          stride value != 1.
        groups: A positive integer specifying the number of groups in which the
          input is split along the channel axis. Each group is convolved
          separately with `filters / groups` filters. The output is the
          concatenation of all the `groups` results along the channel axis. Input
          channels and `filters` must both be divisible by `groups`.
        activation: Activation function to use. If you don't specify anything, no
          activation is applied (see `keras.activations`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix (see
          `keras.initializers`). Defaults to 'glorot_uniform'.
        bias_initializer: Initializer for the bias vector (see
          `keras.initializers`). Defaults to 'zeros'.
        kernel_regularizer: Regularizer function applied to the `kernel` weights
          matrix (see `keras.regularizers`).
        bias_regularizer: Regularizer function applied to the bias vector (see
          `keras.regularizers`).
        activity_regularizer: Regularizer function applied to the output of the
          layer (its "activation") (see `keras.regularizers`).
        kernel_constraint: Constraint function applied to the kernel matrix (see
          `keras.constraints`).
        bias_constraint: Constraint function applied to the bias vector (see
          `keras.constraints`).

    Input shape:
    - If `data_format="channels_last"`:
        A 4D tensor with shape: `(batch_size, height, width, channels)`
    - If `data_format="channels_first"`:
        A 4D tensor with shape: `(batch_size, channels, height, width)`
```

</td>
<td valign="top">

```python
Args:
        filters: Integer, the dimensionality of the output space (i.e. the number
          of output filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the height
          and width of the 2D convolution window. Can be a single integer to
          specify the same value for all spatial dimensions.
        strides: An integer or tuple/list of 2 integers, specifying the strides of
          the convolution along the height and width. Can be a single integer to
          specify the same value for all spatial dimensions. Specifying any stride
          value != 1 is incompatible with specifying any `dilation_rate` value !=
          1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
          `"valid"` means no padding. `"same"` results in padding with zeros
          evenly to the left/right or up/down of the input. When `padding="same"`
          and `strides=1`, the output has the same size as the input.
        data_format: A string, one of `channels_last` (default) or
          `channels_first`.  The ordering of the dimensions in the inputs.
          `channels_last` corresponds to inputs with shape `(batch_size, height,
          width, channels)` while `channels_first` corresponds to inputs with
          shape `(batch_size, channels, height, width)`. It defaults to the
          `image_data_format` value found in your Keras config file at
          `~/.keras/keras.json`. If you never set it, then it will be
          `channels_last`. Note that the `channels_first` format is currently not
          supported by TensorFlow on CPU.
        dilation_rate: an integer or tuple/list of 2 integers, specifying the
          dilation rate to use for dilated convolution. Can be a single integer to
          specify the same value for all spatial dimensions. Currently, specifying
          any `dilation_rate` value != 1 is incompatible with specifying any
          stride value != 1.
        groups: A positive integer specifying the number of groups in which the
          input is split along the channel axis. Each group is convolved
          separately with `filters / groups` filters. The output is the
          concatenation of all the `groups` results along the channel axis. Input
          channels and `filters` must both be divisible by `groups`.
        activation: Activation function to use. If you don't specify anything, no
          activation is applied (see `keras.activations`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix (see
          `keras.initializers`). Defaults to 'glorot_uniform'.
        bias_initializer: Initializer for the bias vector (see
          `keras.initializers`). Defaults to 'zeros'.
        kernel_regularizer: Regularizer function applied to the `kernel` weights
          matrix (see `keras.regularizers`).
        bias_regularizer: Regularizer function applied to the bias vector (see
          `keras.regularizers`).
        activity_regularizer: Regularizer function applied to the output of the
          layer (its "activation") (see `keras.regularizers`).
        kernel_constraint: Constraint function applied to the kernel matrix (see
          `keras.constraints`).
        bias_constraint: Constraint function applied to the bias vector (see
          `keras.constraints`).

    Input shape:
    - If `data_format="channels_last"`:
        A 4D tensor with shape: `(batch_size, height, width, channels)`
    - If `data_format="channels_first"`:
        A 4D tensor with shape: `(batch_size, channels, height, width)`
```

</td>
<td valign="top">

```python
    Args:
        filters: int, the dimension of the output space (the number of filters
            in the convolution).
        kernel_size: int or tuple/list of 2 integer, specifying the size of the
            convolution window.
        strides: int or tuple/list of 2 integer, specifying the stride length
            of the convolution. `strides > 1` is incompatible with
            `dilation_rate > 1`.
        padding: string, either `"valid"` or `"same"` (case-insensitive).
            `"valid"` means no padding. `"same"` results in padding evenly to
            the left/right or up/down of the input such that output has the same
            height/width dimension as the input.
        data_format: string, either `"channels_last"` or `"channels_first"`.
            The ordering of the dimensions in the inputs. `"channels_last"`
            corresponds to inputs with shape
            `(batch_size, channels, height, width)`
            while `"channels_first"` corresponds to inputs with shape
            `(batch_size, channels, height, width)`. It defaults to the
            `image_data_format` value found in your Keras config file at
            `~/.keras/keras.json`. If you never set it, then it will be
            `"channels_last"`.
        dilation_rate: int or tuple/list of 2 integers, specifying the dilation
            rate to use for dilated convolution.
        groups: A positive int specifying the number of groups in which the
            input is split along the channel axis. Each group is convolved
            separately with `filters // groups` filters. The output is the
            concatenation of all the `groups` results along the channel axis.
            Input channels and `filters` must both be divisible by `groups`.
        activation: Activation function. If `None`, no activation is applied.
        use_bias: bool, if `True`, bias will be added to the output.
        kernel_initializer: Initializer for the convolution kernel. If `None`,
            the default initializer (`"glorot_uniform"`) will be used.
        bias_initializer: Initializer for the bias vector. If `None`, the
            default initializer (`"zeros"`) will be used.
        kernel_regularizer: Optional regularizer for the convolution kernel.
        bias_regularizer: Optional regularizer for the bias vector.
        activity_regularizer: Optional regularizer function for the output.
        kernel_constraint: Optional projection function to be applied to the
            kernel after being updated by an `Optimizer` (e.g. used to implement
            norm constraints or value constraints for layer weights). The
            function must take as input the unprojected variable and must return
            the projected variable (which must have the same shape). Constraints
            are not safe to use when doing asynchronous distributed training.
        bias_constraint: Optional projection function to be applied to the
            bias after being updated by an `Optimizer`.
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.667**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.667**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.672**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x1dc9b6f6f517ddf`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.546)</th>
<th align="left">v2-sys (max=0.741)</th>
<th align="left">v2.1-sys (max=0.712)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        learning_rate: A float, a
            `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value for maintaining numerical stability.
        {{base_optimizer_keyword_args}}

    Reference:

    - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
=======
      learning_rate: Initial value for the learning rate: either a floating
        point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
        instance. Defaults to 0.001. Note that `Adadelta` tends to benefit from
        higher initial learning rate values compared to other optimizers. To
        match the exact form in the original paper, use 1.0.
      rho: A `Tensor` or a floating point value. The decay rate. Defaults to
        0.95.
      epsilon: Small floating point value used to maintain numerical stability.
        Defaults to 1e-7.
      {{base_optimizer_keyword_args}}

    Reference:
      - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
>>>>>>> b
    """
```

</td>
<td valign="top">

```python
class AdadeltaOptimizer(tf.keras.optimizers.Optimizer):
    """Adadelta optimizer.

    Adadelta is a stochastic gradient descent variant inspired by the AdaGrad algorithm.
    It is a more sophisticated version of Adagrad that adapts learning rates during training.

    Args:
        learning_rate: A float, a `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A `Tensor` or a floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value used to maintain numerical stability.
            Defaults to `1e-7`.
        {{base_optimizer_keyword_args}}

    Reference:
        - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
    """

    def __init__(self,
                 learning_rate=0.001,
                 rho=0.95,
                 epsilon=1e-7,
                 **kwargs):
        super().__init__(**kwargs)
        self._rho = rho
        self._epsilon = epsilon
        self._learning_rate = learning_rate

    def _resource_apply_dense(self, updates, params):
        grads = self._resource_apply_gradient_transform(updates, params)
        self._update_weights(grads, params)

    def _update_weights(self, grads, params):
        for var, grad in zip(params, grads):
            if grad is not None:
                var.assign(var + self._rho * var - self._epsilon * tf.sqrt(self._rho * var + self._epsilon) * grad)

    def get_config(self):
        config = super().get_config()
        config.update({
            'learning_rate': self._learning_rate,
            'rho': self._rho,
            'epsilon': self._epsilon
        })
        return config

    def get_weights(self):
        return [self._learning_rate, self._rho, self._epsilon]

    def set_weights(self, weights):
        self._learning_rate = weights[0]
        self._rho = weights[1]
        self._epsilon = weights[2]

    def get_learning_rate(self):
        return self._learning_rate

    def set_learning_rate(self, learning_rate):
        self._learning_rate = learning_rate
```

</td>
<td valign="top">

```python
def __init__(
        self,
        learning_rate=0.001,
        rho=0.95,
        epsilon=1e-7,
        {{base_optimizer_keyword_args}}):
        """
        Args:
            learning_rate: Initial value for the learning rate: either a floating
                point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
                instance. Defaults to 0.001. Note that `Adadelta` tends to benefit from
                higher initial learning rate values compared to other optimizers. To
                match the exact form in the original paper, use 1.0.
            rho: A `Tensor` or a floating point value. The decay rate. Defaults to
                0.95.
            epsilon: Small floating point value used to maintain numerical stability.
                Defaults to 1e-7.
            {{base_optimizer_keyword_args}}

        Reference:
            - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
        """
```

</td>
<td valign="top">

```python
def __init__(
        self,
        learning_rate=0.001,
        rho=0.95,
        epsilon=1e-7,
        {{base_optimizer_keyword_args}}):
        """
        Args:
            learning_rate: Initial value for the learning rate: either a floating
                point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
                instance. Defaults to 0.001. Note that `Adadelta` tends to benefit
                from higher initial learning rate values compared to other optimizers.
                To match the exact form in the original paper, use 1.0.
            rho: A `Tensor` or a floating point value. The decay rate. Defaults to
                0.95.
            epsilon: Small floating point value used to maintain numerical stability.
                Defaults to 1e-7.
            {{base_optimizer_keyword_args}}: Additional keyword arguments to be
                passed to the base optimizer.

        Reference:
            - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
        """
```

</td>
<td valign="top">

```python
    Args:
        learning_rate: A float, a
            `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value for maintaining numerical stability.
        {{base_optimizer_keyword_args}}

    Reference:

    - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 3.3× over-gen &nbsp;·&nbsp; max=**0.546**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.741**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.712**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.688)</th>
<th align="left">v2-sys (max=0.772)</th>
<th align="left">v2.1-sys (max=0.995)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
        learning_rate: A float, a
            `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value for maintaining numerical stability.
        {{base_optimizer_keyword_args}}

    Reference:

    - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
=======
      learning_rate: Initial value for the learning rate: either a floating
        point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
        instance. Defaults to 0.001. Note that `Adadelta` tends to benefit from
        higher initial learning rate values compared to other optimizers. To
        match the exact form in the original paper, use 1.0.
      rho: A `Tensor` or a floating point value. The decay rate. Defaults to
        0.95.
      epsilon: Small floating point value used to maintain numerical stability.
        Defaults to 1e-7.
      {{base_optimizer_keyword_args}}

    Reference:
      - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
>>>>>>> b
    """
```

</td>
<td valign="top">

```python
"""
    have been done. Compared to Adagrad, in the original version of Adadelta you
    don't have to set an initial learning rate. In this version, the initial
    learning rate can be set, as in most other Keras optimizers.

    Args:
      learning_rate: Initial value for the learning rate: either a floating
        point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
        instance. Defaults to 0.001. Note that `Adadelta` tends to benefit from
        higher initial learning rate values compared to other optimizers. To
        match the exact form in the original paper, use 1.0.
      rho: A `Tensor` or a floating point value. The decay rate. Defaults to
        0.95.
      epsilon: Small floating point value used to maintain numerical stability.
        Defaults to 1e-7.
      {{base_optimizer_keyword_args}}

    Reference:
      - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
    """

    def __init__(
        self,
        learning_rate=0.001,
        rho=0.95,
```

</td>
<td valign="top">

```python
Args:
        learning_rate: Initial value for the learning rate: either a floating
            point value, or a `tf.keras.optimizers.schedules.LearningRateSchedule`
            instance. Defaults to 0.001. Note that `Adadelta` tends to benefit from
            higher initial learning rate values compared to other optimizers. To
            match the exact form in the original paper, use 1.0.
        rho: A `Tensor` or a floating point value. The decay rate. Defaults to
            0.95.
        epsilon: Small floating point value used to maintain numerical stability.
            Defaults to 1e-7.
        {{base_optimizer_keyword_args}}

    Reference:
      - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
    """
```

</td>
<td valign="top">

```python
Args:
        learning_rate: A float, a
            `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value for maintaining numerical stability.
        {{base_optimizer_keyword_args}}

    Reference:

    - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
    """
```

</td>
<td valign="top">

```python
    Args:
        learning_rate: A float, a
            `keras.optimizers.schedules.LearningRateSchedule` instance, or
            a callable that takes no arguments and returns the actual value to
            use. The learning rate. Defaults to `0.001`. Note that `Adadelta`
            tends to benefit from higher initial learning rate values compared
            to other optimizers. To match the exact form in the original paper,
            use 1.0.
        rho: A floating point value. The decay rate. Defaults to `0.95`.
        epsilon: Small floating point value for maintaining numerical stability.
        {{base_optimizer_keyword_args}}

    Reference:

    - [Zeiler, 2012](http://arxiv.org/abs/1212.5701)
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.688**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.772**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.995**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0x2efe0617463966b3`

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
# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

>>>>>>> b
WINDOWS_BLOCKLIST = [
```

</td>
<td valign="top">

```python
# tests can enable.
TESTS = TESTS + ['doctests']

FSDP_TEST = [test for test in TESTS if test.startswith("distributed/fsdp")]

# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory"
]
```

</td>
<td valign="top">

```python
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory"
]
```

</td>
<td valign="top">

```python
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory"
]
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

**custom** &nbsp;·&nbsp; 1674.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1674.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

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
# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

>>>>>>> b
WINDOWS_BLOCKLIST = [
```

</td>
<td valign="top">

```python
# tests can enable.
TESTS = TESTS + ['doctests']

FSDP_TEST = [test for test in TESTS if test.startswith("distributed/fsdp")]

# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/sync/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory",
```

</td>
<td valign="top">

```python
# Tests can enable.
TESTS = TESTS + ['doctests']

FSDP_TEST = [test for test in TESTS if test.startswith("distributed/fsdp")]

# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory",
```

</td>
<td valign="top">

```python
# tests can enable.
TESTS = TESTS + ['doctests']

FSDP_TEST = [test for test in TESTS if test.startswith("distributed/fsdp")]

# Tests need to be run with pytest.
USE_PYTEST_LIST = [
    "distributed/pipeline/sync/skip/test_api",
    "distributed/pipeline/sync/skip/test_gpipe",
    "distributed/pipeline/sync/skip/test_inspect_skip_layout",
    "distributed/pipeline/sync/skip/test_leak",
    "distributed/pipeline/sync/skip/test_portal",
    "distributed/pipeline/skip/test_stash_pop",
    "distributed/pipeline/sync/skip/test_tracker",
    "distributed/pipeline/sync/skip/test_verify_skippables",
    "distributed/pipeline/sync/test_balance",
    "distributed/pipeline/sync/test_bugs",
    "distributed/pipeline/sync/test_checkpoint",
    "distributed/pipeline/sync/test_copy",
    "distributed/pipeline/sync/test_deferred_batch_norm",
    "distributed/pipeline/sync/test_dependency",
    "distributed/pipeline/sync/test_inplace",
    "distributed/pipeline/sync/test_microbatch",
    "distributed/pipeline/sync/test_phony",
    "distributed/pipeline/sync/test_pipe",
    "distributed/pipeline/sync/test_pipeline",
    "distributed/pipeline/sync/test_stream",
    "distributed/pipeline/sync/test_transparency",
    "distributed/pipeline/sync/test_worker",
    "distributions/test_constraints",
    "distributions/test_transforms",
    "distributions/test_utils",
    "test_typing",
    "distributed/elastic/events/lib_test",
    "distributed/elastic/agent/server/test/api_test",
    "test_deploy",
    "distributed/test_c10d_error_logger"
]

WINDOWS_BLOCKLIST = [
    "test_ops_jit",  # TODO: Broken on Windows https://github.com/pytorch/pytorch/issues/96858
    "distributed/nn/jit/test_instantiator",
    "distributed/rpc/test_faulty_agent",
    "distributed/rpc/test_tensorpipe_agent",
    "distributed/rpc/test_share_memory",
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

**pick-b** &nbsp;·&nbsp; 1836.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1831.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1831.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x7ddbe8f8a186416`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.085)</th>
<th align="left">v2-sys (max=0.081)</th>
<th align="left">v2.1-sys (max=0.081)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
                if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
<<<<<<< a
        elif name in ("backward", "data_ptr", "coalesce"):
=======
        elif name in ("backward", "data_ptr"):
>>>>>>> b
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

```

</td>
<td valign="top">

```python
tx,
                        sub_proxy.item(),
                        sym_num=tx.output.shape_env.create_unbacked_symint(),
                    )

                if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
```

</td>
<td valign="top">

```python
if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
                unimplemented(f"Tensor.__setitem__ with boolean key and gradient tensor")
            else:
                return self.call_method(tx, "__setitem__", [key, value], {})
```

</td>
<td valign="top">

```python
if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)

        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
                unimplemented(f"Tensor.__setitem__ with boolean key and gradient tensor")
            else:
                return self.call_method(tx, "__setitem__", [key, value], {})
```

</td>
<td valign="top">

```python
    def method_tolist(self):
        from ..symbolic_convert import InstructionTranslator
        from .builder import SourcelessBuilder

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 13.4× over-gen &nbsp;·&nbsp; max=**0.085**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 13.5× over-gen &nbsp;·&nbsp; max=**0.081**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 13.6× over-gen &nbsp;·&nbsp; max=**0.081**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.090)</th>
<th align="left">v2-sys (max=0.090)</th>
<th align="left">v2.1-sys (max=0.090)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
                if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
<<<<<<< a
        elif name in ("backward", "data_ptr", "coalesce"):
=======
        elif name in ("backward", "data_ptr"):
>>>>>>> b
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

```

</td>
<td valign="top">

```python
if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
```

</td>
<td valign="top">

```python
if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
```

</td>
<td valign="top">

```python
if tensor.dtype not in [
                    torch.int8,
                    torch.int16,
                    torch.int32,
                    torch.int64,
                ]:
                    unimplemented("Input tensor for tolist must be an integer tensor")

                if tensor.dim() == 0:
                    return wrap(tensor, sub_proxy)

                if tensor.dim() == 1:
                    return [wrap(val, sub_proxy[i]) for i, val in enumerate(tensor)]

                return [
                    tolist(sub_tensor, sub_proxy=sub_proxy[i])
                    for i, sub_tensor in enumerate(tensor)
                ]

            tensor = self.as_proxy().node.meta["example_value"]
            out = tolist(tensor, self.as_proxy())
            return SourcelessBuilder()(tx, out)
        elif name in ("backward", "data_ptr"):
            unimplemented(f"Tensor.{name}")
        elif name == "item" and not config.capture_scalar_outputs:
            unimplemented(f"Tensor.{name}")
        elif name == "__len__":
            return self.call_method(tx, "size", [ConstantVariable.create(0)], {})
        elif name == "__setitem__":
            key, value = args

            def has_bool_key(v):
                if isinstance(v, TensorVariable):
                    return v.dtype in (torch.bool, torch.int8)
                elif isinstance(v, TupleVariable):
                    return any(has_bool_key(item) for item in v.items)
                else:
                    return False

            if (
                has_bool_key(key)
                and isinstance(value, TensorVariable)
                and value.requires_grad
            ):
```

</td>
<td valign="top">

```python
    def method_tolist(self):
        from ..symbolic_convert import InstructionTranslator
        from .builder import SourcelessBuilder

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 12.2× over-gen &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 12.2× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 12.2× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
