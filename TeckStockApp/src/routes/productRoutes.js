const express = require('express');
const router = express.Router();
const ProductController = require('../controllers/productController');

router.get('/', ProductController.index);
router.get('/new', ProductController.showCreate);
router.post('/', ProductController.create);
router.get('/:id/edit', ProductController.showEdit);
router.post('/:id/update', ProductController.update);
router.post('/:id/delete', ProductController.delete);

module.exports = router;
