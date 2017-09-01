import DS from 'ember-data';

export default DS.Model.extend({
  department: DS.belongsTo('department'),
  person: DS.belongsTo('person'),
  info: DS.attr('string'),
});
