
const USERS = [
  { username: 'admin', password: 'admin123', role: 'admin' },
  { username: 'user', password: 'user123', role: 'user' }
];

const AuthController = {
  showLogin(req, res) {
    if (req.session.user) {
      return res.redirect('/dashboard');
    }
    res.render('login', { title: 'Login - TechStock', layout: false });
  },

  login(req, res) {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.render('login', {
        title: 'Login - TechStock',
        layout: false,
        error: 'Por favor ingresa usuario y contraseña.'
      });
    }

    const user = USERS.find(
      u => u.username === username && u.password === password
    );

    if (!user) {
      return res.render('login', {
        title: 'Login - TechStock',
        layout: false,
        error: 'Usuario o contraseña incorrectos.'
      });
    }

    req.session.user = { username: user.username, role: user.role };
    res.redirect('/dashboard');
  },

  logout(req, res) {
    req.session.destroy(() => {
      res.redirect('/login');
    });
  }
};

module.exports = AuthController;
