# Course scheduler demo


## Example run

```
Fetching 'Courses to Schedule!A2:J'
Fetching 'Rooms!A2:B'
Fetching 'Blocks!A2:C'
Fetching 'Occupied Times!A2:D'
Fetching 'Config!A2:B'
Building internal representation.
Generating 399 variables for course='MTH 1' days=MW block=0
Generating 231 variables for course='MTH 1' days=MW block=1
Generating 203 variables for course='MTH 1' days=MW block=2
Generating 119 variables for course='MTH 1' days=MW block=3
Generating 399 variables for course='MTH 1' days=TR block=0
Generating 231 variables for course='MTH 1' days=TR block=1
Generating 203 variables for course='MTH 1' days=TR block=2
Generating 119 variables for course='MTH 1' days=TR block=3
Generating 399 variables for course='MTH 1' days=MTWR block=0
Generating 203 variables for course='MTH 1' days=MTWR block=2
Generating 399 variables for course='MTH 47' days=MW block=0
Generating 231 variables for course='MTH 47' days=MW block=1
Generating 203 variables for course='MTH 47' days=MW block=2
Generating 203 variables for course='MTH 47' days=TR block=2
Generating 119 variables for course='MTH 47' days=TR block=3
Generating 399 variables for course='MTH 47S' days=MTR block=0
Generating 231 variables for course='MTH 47S' days=MTR block=1
Generating 203 variables for course='MTH 47S' days=MTR block=2
Generating 119 variables for course='MTH 47S' days=MW block=3
Generating 231 variables for course='MTH 47S' days=MWF block=1
Created 11956 class start variables
Built 48 uniqueness constraints
Built 11956 conflict constraints
Built 11956 meeting consistency constraints
Converting to ortools model.
Starting solve.
Finished solve, status=0.
ClassStart_MTH 1-MTWR-0_M_0835_1758 = 1
ClassStart_MTH 1-MTWR-0_R_0835_1758 = 1
ClassStart_MTH 1-MTWR-0_T_0835_1758 = 1
ClassStart_MTH 1-MTWR-0_W_0835_1758 = 1
ClassStart_MTH 1-MTWR-2_M_1700_1756 = 1
ClassStart_MTH 1-MTWR-2_R_1700_1756 = 1
ClassStart_MTH 1-MTWR-2_T_1700_1756 = 1
ClassStart_MTH 1-MTWR-2_W_1700_1756 = 1
ClassStart_MTH 1-MW-0_M_0920_test3 = 1
ClassStart_MTH 1-MW-0_W_0920_test3 = 1
ClassStart_MTH 1-MW-1_M_1235_1757 = 1
ClassStart_MTH 1-MW-1_W_1235_1757 = 1
ClassStart_MTH 1-MW-2_M_1510_1755 = 1
ClassStart_MTH 1-MW-2_W_1510_1755 = 1
ClassStart_MTH 1-MW-3_M_1900_test4 = 1
ClassStart_MTH 1-MW-3_W_1900_test4 = 1
ClassStart_MTH 1-TR-0_R_1145_1755 = 1
ClassStart_MTH 1-TR-0_T_1145_1755 = 1
ClassStart_MTH 1-TR-1_R_1210_1758 = 1
ClassStart_MTH 1-TR-1_T_1210_1758 = 1
ClassStart_MTH 1-TR-2_R_1625_1752 = 1
ClassStart_MTH 1-TR-2_T_1625_1752 = 1
ClassStart_MTH 1-TR-3_R_1910_1757 = 1
ClassStart_MTH 1-TR-3_T_1910_1757 = 1
ClassStart_MTH 47-MW-0_M_0935_1758 = 1
ClassStart_MTH 47-MW-0_W_0935_1758 = 1
ClassStart_MTH 47-MW-1_M_1215_1758 = 1
ClassStart_MTH 47-MW-1_W_1215_1758 = 1
ClassStart_MTH 47-MW-2_M_1530_1758 = 1
ClassStart_MTH 47-MW-2_W_1530_1758 = 1
ClassStart_MTH 47-TR-2_R_1630_1757 = 1
ClassStart_MTH 47-TR-2_T_1630_1757 = 1
ClassStart_MTH 47-TR-3_R_1820_test3 = 1
ClassStart_MTH 47-TR-3_T_1820_test3 = 1
ClassStart_MTH 47S-MTR-0_M_0720_1758 = 1
ClassStart_MTH 47S-MTR-0_R_0720_1758 = 1
ClassStart_MTH 47S-MTR-0_T_0720_1758 = 1
ClassStart_MTH 47S-MTR-1_M_1305_test4 = 1
ClassStart_MTH 47S-MTR-1_R_1305_test4 = 1
ClassStart_MTH 47S-MTR-1_T_1305_test4 = 1
ClassStart_MTH 47S-MTR-2_M_1550_1757 = 1
ClassStart_MTH 47S-MTR-2_R_1550_1757 = 1
ClassStart_MTH 47S-MTR-2_T_1550_1757 = 1
ClassStart_MTH 47S-MW-3_M_1855_1756 = 1
ClassStart_MTH 47S-MW-3_W_1855_1756 = 1
ClassStart_MTH 47S-MWF-1_F_1335_1758 = 1
ClassStart_MTH 47S-MWF-1_M_1335_1758 = 1
ClassStart_MTH 47S-MWF-1_W_1335_1758 = 1
python model.py  9.08s user 0.50s system 72% cpu 13.240 total
```
