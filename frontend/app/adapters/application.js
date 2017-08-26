import Ember from 'ember';
import DRFAdapter from './drf';

export default DRFAdapter.extend({
    addTrailingSlashes: false,

    urlForFindRecord(id, modelName, snapshot) {
        let url = this._super(...arguments);
        let query = Ember.get(snapshot, 'adapterOptions.query');
        if (query) {
            url += '?' + Ember.$.param(query); // assumes no query params are present already
        }
        return url;
    }
});
