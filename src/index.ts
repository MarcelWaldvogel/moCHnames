import namemap from "./data/name.json";
import plzmap from "./data/plz.json";

export const cantons = [
  "ZH",
  "BE",
  "LU",
  "UR",
  "SZ",
  "OW",
  "NW",
  "GL",
  "ZG",
  "FR",
  "SO",
  "BS",
  "BL",
  "SH",
  "AR",
  "AI",
  "SG",
  "GR",
  "AG",
  "TG",
  "TI",
  "VD",
  "VS",
  "NE",
  "GE",
  "JU",
] as const;
export type Canton = typeof cantons[number];

export type Gender = "m" | "f";
export type NameLocation = {
  first: string;
  last: string;
  gender: Gender;
  plz: string;
  town: string;
  townNoCanton: string; // Guaranteed not to end in the canton
  canton: Canton;
};
type Array1Plus<T> = [T, ...T[]];
export type NameMap = Record<
  string,
  {
    f: [Array1Plus<string>, Array1Plus<string>];
    m: [Array1Plus<string>, Array1Plus<string>];
    l: string;
    c: Canton;
  }
>;
type ImportedNameMap = Record<
  string,
  {
    f: string[][];
    m: string[][];
    l: string;
    c: Canton;
  }
>;
type PlzMap = Record<string, [string, string]>;
type ImportedPlzMap = Record<string, string[]>;
export const nameMap = namemap as ImportedNameMap as NameMap;
export const plzMap = plzmap as ImportedPlzMap as PlzMap;

const cantonNameMapCache: Partial<Record<Canton, NameMap>> = {};
function cantonNameMap(canton: Canton): NameMap {
  if (canton in cantonNameMapCache) {
    return cantonNameMapCache[canton] as NameMap;
  } else {
    const names = Object.fromEntries(
      Object.entries(nameMap).filter(([key, value]) => value.c === canton)
    );
    cantonNameMapCache[canton] = names;
    return names;
  }
}

function getRandomInt(max: number) {
  return Math.floor(Math.random() * max);
}
function pickRandom<T>(input: T[]): T {
  return input[getRandomInt(input.length)];
}

function removeTrailingCanton(town: string, canton: Canton) {
  if (town.endsWith(` ${canton}`)) {
    return town.substring(0, town.length - 3);
  } else {
    return town;
  }
}

/**
 * Return a random mock person, whose name matches the most common names
 * at that location.
 * The report frequency of a location depends on the number of postal codes,
 * not on their population.
 * WARNING: Does not provide cryptographic unpredictability!
 *
 * @param canton Optional canton (default: all of Switzerland)
 * @returns A random `NameLocation`
 */
export function mockNameLocation(canton?: Canton): NameLocation {
  const names = canton === undefined ? nameMap : cantonNameMap(canton);
  const plzs = Object.keys(names);
  const plz = pickRandom(plzs);
  const record = names[plz];
  const gender: Gender = pickRandom(["f", "m"]);
  const [firsts, lasts] = record[gender];
  const first = pickRandom(firsts);
  const last = pickRandom(lasts);
  const townCanton = record.c;

  return {
    first,
    last,
    gender,
    plz,
    town: record.l,
    townNoCanton: removeTrailingCanton(record.l, townCanton),
    canton: townCanton,
  };
}

/*
for (let i = 0; i < 100; i++) {
  console.log(mockNameLocation());
}
*/
