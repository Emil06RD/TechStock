const ProductModel = require('../models/productModel');

const ProductController = {

  index(req, res) {
    const products = ProductModel.getAll();
    res.render('products/index', {
      title: 'Productos - TechStock',
      products,
      user: req.session.user
    });
  },


  showCreate(req, res) {
    res.render('products/form', {
      title: 'Nuevo Producto - TechStock',
      product: {},
      isEdit: false,
      user: req.session.user
    });
  },


  create(req, res) {
    const { name, price, quantity, category } = req.body;
    const errors = validateProduct(req.body);

    if (errors.length > 0) {
      return res.render('products/form', {
        title: 'Nuevo Producto - TechStock',
        product: req.body,
        isEdit: false,
        errors,
        user: req.session.user
      });
    }

    ProductModel.create({ name, price, quantity, category });
    res.redirect('/products');
  },


  showEdit(req, res) {
    const product = ProductModel.getById(req.params.id);
    if (!product) {
      return res.status(404).send('Producto no encontrado');
    }
    res.render('products/form', {
      title: 'Editar Producto - TechStock',
      product,
      isEdit: true,
      user: req.session.user
    });
  },


  update(req, res) {
    const { name, price, quantity, category } = req.body;
    const errors = validateProduct(req.body);

    if (errors.length > 0) {
      const product = { ...req.body, id: req.params.id };
      return res.render('products/form', {
        title: 'Editar Producto - TechStock',
        product,
        isEdit: true,
        errors,
        user: req.session.user
      });
    }

    ProductModel.update(req.params.id, { name, price, quantity, category });
    res.redirect('/products');
  },


  delete(req, res) {
    ProductModel.delete(req.params.id);
    res.redirect('/products');
  }
};

function validateProduct({ name, price, quantity, category }) {
  const errors = [];
  if (!name || name.trim() === '') errors.push('El nombre es obligatorio.');
  if (!price || price === '') errors.push('El precio es obligatorio.');
  else if (isNaN(parseFloat(price)) || parseFloat(price) < 0) errors.push('El precio debe ser un número válido mayor o igual a 0.');
  if (!quantity || quantity === '') errors.push('La cantidad es obligatoria.');
  else if (!Number.isInteger(Number(quantity)) || parseInt(quantity) < 0) errors.push('La cantidad debe ser un número entero mayor o igual a 0.');
  if (!category || category.trim() === '') errors.push('La categoría es obligatoria.');
  return errors;
}

module.exports = ProductController;
