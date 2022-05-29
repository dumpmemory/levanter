# Very similar to the equinox version, but it makes the fields static, which works better with optax
from typing import Optional

import equinox as eqx
from equinox.custom_types import Array

import jax.random as jrandom
import jax.numpy as jnp


class Dropout(eqx.Module):
    """Applies dropout."""

    # key difference from equinox: these are static fields
    p: float = eqx.static_field()

    def __init__(
        self,
        p: float = 0.5,
    ):
        """**Arguments:**

        - `p`: The fraction of entries to set to zero. (On average.)
        """

        self.p = p

    def __call__(
        self,
        x: Array,
        *,
        inference: bool,
        key: Optional["jax.random.PRNGKey"] = None,
    ) -> Array:
        """**Arguments:**

        - `x`: An any-dimensional JAX array to dropout.
        - `key`: A `jax.random.PRNGKey` used to provide randomness for calculating
            which elements to dropout. (Keyword only argument.)
        - `inference`: As per [`equinox.nn.Dropout.__init__`][]. If `True` or
            `False` then it will take priority over `self.inference`. If `None`
            then the value from `self.inference` will be used.
        - `deterministic`: Deprecated alternative to `inference`.
        """

        if isinstance(self.p, (int, float)) and self.p == 0:
            inference = True
        if inference:
            return x
        elif key is None:
            raise RuntimeError(
                "Dropout requires a key when running in non-deterministic mode."
            )
        else:
            q = 1 - self.p
            mask = jrandom.bernoulli(key, q, x.shape)
            return jnp.where(mask, x / q, 0)