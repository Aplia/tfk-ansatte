import DS from 'ember-data';

export default DS.Model.extend({
  positions: DS.hasMany('position'),
  familyName: DS.attr('string'),
  givenName: DS.attr('string'),
  email: DS.attr('string'),
  mobilePhone: DS.attr('string'),
  workPhone: DS.attr('string'),
});
