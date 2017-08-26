
import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('is-department-selected', 'helper:is-department-selected', {
  integration: true
});

// Replace this with your real tests.
test('it renders', function(assert) {
  this.set('inputValue', '1234');

  this.render(hbs`{{is-department-selected inputValue}}`);

  assert.equal(this.$().text().trim(), '1234');
});

