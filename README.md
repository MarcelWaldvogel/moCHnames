# Swiss Mock names

## Data sources

This database of mock Swiss names is based on the following data:

- [`vornamen_proplz`](https://swisspost.opendatasoft.com/explore/dataset/vornamen_proplz/information/):
  CC-BY, Die Schweizerische Post (2022-07-01)
- [`nachnamen_proplz`](https://swisspost.opendatasoft.com/explore/dataset/nachnamen_proplz/information/):
  CC-BY, Die Schweizerische Post (2022-07-01)
- [`plz_verzeichnis_v2`](https://swisspost.opendatasoft.com/explore/dataset/plz_verzeichnis_v2/information/):
  CC-BY, Die Schweizerische Post (2022-07-11)

## Data format

### Raw data

For description of the `raw/` data, see the Swiss Post descriptions above.

### Processed data

The data in `src/data/` is JSON matching the following TypeScript types:

```typescript
type NameMap = Record<
  string,
  {
    f: [Array1Plus<string>, Array1Plus<string>];
    m: [Array1Plus<string>, Array1Plus<string>];
    l: string;
    c: Canton;
  }
>;
type PlzMap = Record<string, [string, string]>;
```

where `Array1Plus<string>` is an array of at least one string (maximum five, due
to the format of the Swiss Post data). Any PLZ (postal code) area which does not
have at least one male/female first/last name each, will be filtered out. (E.g.
"8261 Hemishofen" is missing, because the raw data does not contain any female
first names. The raw files include name information only, when more than five
people have the same name.)

### JavaScript/TypeScript API

Install the module as follows:

```sh
npm i moCHnames
# or
yarn add moCHnames
```

Use as follows to get a mock person from anywhere in Switzerland:

```typescript
import { mockNameLocation } from "moCHnames";

console.log(mockNameLocation());
```

Possible output:

```typescript
{
  first: 'Martin',
  last: 'Meier',
  gender: 'm',
  plz: '7208',
  town: 'Malans GR',
  townNoCanton: 'Malans',
  canton: 'GR'
}
```

To only get mock people from a particular canton, pass the canton's two-letter
abbreviation (e.g., `SH`) as an optional parameter to `mockNameLocation()`.
