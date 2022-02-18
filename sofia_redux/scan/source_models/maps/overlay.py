# Licensed under a 3-clause BSD style license - see LICENSE.rst

from sofia_redux.scan.source_models.maps.image import Image

__all__ = ['Overlay']


class Overlay(Image):

    def __init__(self, data=None, blanking_value=None, dtype=None,
                 shape=None, unit=None):
        """
        Create an overlay of an underlying image.

        The overlay object is an interface to a basis image.  Multiple overlays
        can be applied to a single image allowing the data to be accessed and
        set as desired.

        Parameters
        ----------
        data : numpy.ndarray or FlaggedArray or Image or Overlay, optional
            The image to overlay.
        blanking_value : int or float, optional
            The value indicating that a data value is invalid.
        dtype : type, optional
            The data type.
        shape : tuple of int, optional
            The shape of the data.
        unit : astropy.units.Quantity, optional
            The data unit.
        """
        if not isinstance(data, Image):
            basis = Image(data=data, blanking_value=blanking_value,
                          dtype=dtype, shape=shape, unit=unit)
        else:
            basis = data

        self.basis = None
        self.set_basis(basis)
        if isinstance(self.basis, Image):
            if unit is None:
                unit = self.basis.unit
            if dtype is None:
                dtype = self.basis.dtype
            if blanking_value is None:
                blanking_value = self.basis.blanking_value

        super().__init__(blanking_value=blanking_value, dtype=dtype,
                         shape=shape, unit=unit)

    @property
    def data(self):
        return self.basis.data

    @data.setter
    def data(self, values):
        self.basis.data = values

    @property
    def flag(self):
        return self.basis.flag

    @flag.setter
    def flag(self, values):
        self.basis.flag = values

    @property
    def valid(self):
        return self.basis.valid

    @property
    def blanking_value(self):
        return self.basis.blanking_value

    @blanking_value.setter
    def blanking_value(self, value):
        self.basis.blanking_value = value

    @property
    def fixed_index(self):
        return self.basis.fixed_index

    @fixed_index.setter
    def fixed_index(self, values):
        self.basis.fixed_index = values

    @property
    def dtype(self):
        return self.basis.dtype

    @dtype.setter
    def dtype(self, value):
        self.basis.dtype = value

    @property
    def shape(self):
        return self.basis.shape

    @shape.setter
    def shape(self, new_shape):
        self.set_data_shape(new_shape)

    @property
    def size(self):
        return self.basis.size

    @property
    def ndim(self):
        return self.basis.ndim

    def copy(self, with_contents=True):
        """
        Return a copy of the overlay.

        Parameters
        ----------
        with_contents : bool, optional
            If `True`, paste the contents of this image onto the new one.

        Returns
        -------
        Overlay
        """
        return super().copy(with_contents=with_contents)

    def set_basis(self, basis):
        """
        Set the basis image.

        Parameters
        ----------
        basis : Image or FitsData or FlaggedArray

        Returns
        -------
        None
        """
        self.basis = basis

    def set_data(self, data, change_type=False):
        """
        Set the data of the flagged array.

        All flags are set to zero.

        Parameters
        ----------
        data : numpy.ndarray or FlaggedArray
        change_type : bool, optional
            If `True`, change the data type to that of the data.

        Returns
        -------
        None
        """
        self.basis.set_data(data, change_type=change_type)

    def set_data_shape(self, shape):
        """
        Set the shape of the data array.

        Parameters
        ----------
        shape : tuple (int)

        Returns
        -------
        None
        """
        self.basis.set_data_shape(shape)

    def destroy(self):
        """
        Destroy the basis image.

        Returns
        -------
        None
        """
        if self.basis is not None:
            self.basis.destroy()

    def crop(self, ranges):
        """
        Crop the overlay to the required dimensions.

        Parameters
        ----------
        ranges : numpy.ndarray (int,)
            The ranges to set crop the data to.  Should be of shape
            (n_dimensions, 2) where ranges[0, 0] would give the minimum crop
            limit for the first dimension and ranges[0, 1] would give the
            maximum crop limit for the first dimension.  In this case, the
            'first' dimension is in numpy format.  i.e., (y, x) for a 2-D
            array. Also note that the upper crop limit is not inclusive so
            a range of (0, 3) includes indices [0, 1, 2] but not 3.

        Returns
        -------
        None
        """
        if self.basis is not None:
            self.basis.crop(ranges)