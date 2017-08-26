import DRFSerializer from './drf';
import DS from 'ember-data';

export default DRFSerializer.extend(DS.EmbeddedRecordsMixin, {
    attrs: {
        department: { embedded: 'always' },
        person: { embedded: 'always' }
    }
});
