const express = require('express');
const session = require('express-session');
const { engine } = require('express-handlebars');
const path = require('path');

const authRoutes = require('./routes/authRoutes');
const productRoutes = require('./routes/productRoutes');
const { requireAuth } = require('./middleware/authMiddleware');

const app = express();
const PORT = 3000;


app.engine('hbs', engine({
  extname: '.hbs',
  defaultLayout: 'main',
  layoutsDir: path.join(__dirname, 'views/layouts'),
  partialsDir: path.join(__dirname, 'views/partials'),
  helpers: {
    eq: (a, b) => a === b
  }
}));
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'views'));


app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
  secret: 'techstock-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 }
}));


app.use('/', authRoutes);
app.use('/products', requireAuth, productRoutes);


app.get('/', (req, res) => {
  if (req.session.user) {
    res.redirect('/dashboard');
  } else {
    res.redirect('/login');
  }
});


app.get('/dashboard', requireAuth, (req, res) => {
  res.render('dashboard', {
    title: 'Dashboard - TechStock',
    user: req.session.user
  });
});

app.listen(PORT, () => {
  console.log(`✅ TechStock corriendo en http://localhost:${PORT}`);
});

module.exports = app;
