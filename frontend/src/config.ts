import configJson from '../../config.json';
import { ConfigSchema } from './zodSchemas';

const config = ConfigSchema.parse(configJson);

export default config;