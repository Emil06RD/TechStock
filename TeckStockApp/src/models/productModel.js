const db = require('./db');

const ProductModel = {
  getAll() {
    return db.prepare('SELECT * FROM products ORDER BY id DESC').all();
  },

  getById(id) {
    return db.prepare('SELECT * FROM products WHERE id = ?').get(parseInt(id)) || null;
  },

  create({ name, price, quantity, category }) {
    const stmt = db.prepare(
      'INSERT INTO products (name, price, quantity, category, created_at) VALUES (?, ?, ?, ?, ?)'
    );
    const info = stmt.run(
      name.trim(),
      parseFloat(price),
      parseInt(quantity),
      category.trim(),
      new Date().toISOString()
    );
    return info.lastInsertRowid;
  },

  update(id, { name, price, quantity, category }) {
    const stmt = db.prepare(
      'UPDATE products SET name = ?, price = ?, quantity = ?, category = ? WHERE id = ?'
    );
    const info = stmt.run(
      name.trim(),
      parseFloat(price),
      parseInt(quantity),
      category.trim(),
      parseInt(id)
    );
    return info.changes > 0;
  },

  delete(id) {
    const info = db.prepare('DELETE FROM products WHERE id = ?').run(parseInt(id));
    return info.changes > 0;
  }
};

module.exports = ProductModel;
