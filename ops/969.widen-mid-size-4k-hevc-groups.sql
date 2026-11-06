-- @description: Widen the compact ladder with the other mid-size and small 4K HEVC groups
-- @author: cursor
-- @name: 969.widen-mid-size-4k-hevc-groups

BEGIN TRANSACTION;

UPDATE regular_expressions SET pattern = '(?i)(?:^\[(?:TimeDistortion|bluegreeen|Chivaman|edge2020|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer)\]|(?:^|[-.\s(\[])(?:TimeDistortion|bluegreeen|Chivaman|edge2020|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', description = 'Careful and mid-size 4K circles: HONE, hallowed, Vyndros, edge2020, dkore, HQMUX, PTer.' WHERE name = 'HEVC Compact Elite';

UPDATE regular_expressions SET pattern = '(?i)(?:^\[(?:FreetheFish|Nostradamus|DrainedDay|Species180|BHDStudio|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)\]|(?:^|[-.\s(\[])(?:FreetheFish|Nostradamus|DrainedDay|Species180|BHDStudio|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', description = 'QxR and TAoE circles plus BHDStudio, HeVK, KeepFRDS and Prof.' WHERE name = 'HEVC Compact Circle';

UPDATE regular_expressions SET pattern = '(?i)(?:^\[(?:D0ct0rLew|DEFLATE|IAMABLE|POOTLED|PSARips|PSYPHER|ReELiTE|kronox|LEGi0N|yawnix|ELiTE|HiQVE|HODL|Kira|d3g|PSA|SEV|SIQ)\]|(?:^|[-.\s(\[])(?:D0ct0rLew|DEFLATE|IAMABLE|POOTLED|PSARips|PSYPHER|ReELiTE|kronox|LEGi0N|yawnix|ELiTE|HiQVE|HODL|Kira|d3g|PSA|SEV|SIQ)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', description = 'Smaller 4K HEVC that still holds up on a 55-inch Mini LED: PSA, d3g, SEV, ELiTE, HiQVE, HODL, DEFLATE and peers.' WHERE name = 'HEVC Compact Small';

UPDATE regular_expressions SET pattern = '(?i)(?:^\[(?:UTRcorp|RARBG|t0paz|iVy|Joy|POF|UTR)\]|(?:^|[-.\s(\[])(?:UTRcorp|RARBG|t0paz|iVy|Joy|POF|UTR)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', description = 'Watchable smaller encodes: UTR/Joy, RARBG, iVy, t0paz, POF. Upgraded when a better group exists.' WHERE name = 'HEVC Compact Micro OK';

UPDATE quality_profiles SET description = 'Compact 4K HEVC for a 55-inch Mini LED and a 32-inch 4K monitor. HONE, hallowed, HQMUX and PTer first, then QxR/TAoE/BHDStudio, then PSA/HiQVE/DEFLATE, then UTR/RARBG/iVy. YTS and MeGusta stay rejected.' WHERE name = 'Movies 2160p HEVC Compact';
UPDATE quality_profiles SET description = 'Compact 4K HEVC episodes for the same screens. WEB from those circles first, then disc. The smaller groups can fill gaps. YTS and MeGusta stay rejected.' WHERE name = 'TV 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('hallowed is in the top circle', (SELECT pattern LIKE '%hallowed%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('BHDStudio is in the QxR circle', (SELECT pattern LIKE '%BHDStudio%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('HiQVE is in the small tier', (SELECT pattern LIKE '%HiQVE%' FROM regular_expressions WHERE name = 'HEVC Compact Small')),
  ('KONTRAST stays out', (SELECT count(*) = 0 FROM regular_expressions WHERE name LIKE 'HEVC Compact%' AND pattern LIKE '%KONTRAST%')),
  ('YTS stays banned', (SELECT pattern LIKE '%YTS%' FROM regular_expressions WHERE name = 'HEVC Compact Micro Ban'));
DROP TABLE _pcd_assertions;
COMMIT;
