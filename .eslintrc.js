module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  extends: ['@nuxt/eslint-config', 'plugin:prettier/recommended'],
  plugins: ['prettier'],
  rules: {
    'prettier/prettier': 'error',
    'no-console': 'warn'
  }
}