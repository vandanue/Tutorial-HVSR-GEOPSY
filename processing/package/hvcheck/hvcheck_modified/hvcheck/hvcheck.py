from numpy import *

def hvsrcheck(indict):
    print("-----------------------------------------------------------------------")
    print(f"File Name\t\t: {indict['filename']}")
    print("-----------------------------------------------------------------------")
    print("CRITERIA FOR A RELIABLE H/V CURVE")
    print("-----------------------------------------------------------------------")
    
    # Reliable H/V Curve Criteria
    print("\nChecking reliable H/V criteria...\n")
    if indict['F0'] > (10 / indict['winlength']):
        print(f"RELIABLE 1 - OK\t\t: f0 > 10/lw = {indict['F0']} > {10 / indict['winlength']}")
    else:
        print(f"RELIABLE 1 - NO\t\t: f0 < 10/lw = {indict['F0']} < {10 / indict['winlength']}")

    nc = indict['winlength'] * indict['window'] * indict['F0']
    if nc > 200:
        print(f"RELIABLE 2 - OK\t\t: nc(f0) > 200 = {nc} > 200")
    else:
        print(f"RELIABLE 2 - NO\t\t: nc(f0) < 200 = {nc} < 200")
    
    idfr1 = where(indict['frhv'] > 0.5 * indict['F0'])[0]
    idfr2 = where(indict['frhv'] < 2 * indict['F0'])[0]
    r31 = all(indict['stdhv'][idfr1] < 2) if len(idfr1) > 0 else False
    r32 = all(indict['stdhv'][idfr2] < 2) if len(idfr2) > 0 else False
    if (r31 and r32):
        print(f"RELIABLE 3 - OK\t\t: Std H/V(f) < 2")
    else:
        print(f"RELIABLE 3 - NO\t\t: Std H/V(f) > 2")

    print("\n-----------------------------------------------------------------------")
    print("CLEAR PEAK FOR H/V CURVE")
    print("-----------------------------------------------------------------------")
    
    # Clear Peak Criteria
    print("\nChecking clear peak criteria...\n")
    clear_count = []
    
    # (1) H/V(f-) < A0/2 for f0/4 to f0
    idfr1 = where((indict['frhv'] >= indict['F0'] / 4) & (indict['frhv'] <= indict['F0']))[0]
    if len(idfr1) > 0 and any(indict['hvsr'][idfr1] < indict['A0'] / 2):
        cc = 1
        print(f"CLEAR PEAK 1 - OK\t: A(f-) < A0/2 = {indict['A0'] / 2}")
    else:
        cc = 0
        print(f"CLEAR PEAK 1 - NO\t: A(f-) >= A0/2 = {indict['A0'] / 2}")
    clear_count.append(cc)
    
    # (2) H/V(f+) < A0/2 for f0 to 4f0
    idfr2 = where((indict['frhv'] >= indict['F0']) & (indict['frhv'] <= 4 * indict['F0']))[0]
    if len(idfr2) > 0 and any(indict['hvsr'][idfr2] < indict['A0'] / 2):
        cc = 1
        print(f"CLEAR PEAK 2 - OK\t: A(f+) < A0/2 = {indict['A0'] / 2}")
    else:
        cc = 0
        print(f"CLEAR PEAK 2 - NO\t: A(f+) >= A0/2 = {indict['A0'] / 2}")
    clear_count.append(cc)
    
    # (3) A0 > 2
    if indict['A0'] > 2:
        cc = 1
        print(f"CLEAR PEAK 3 - OK\t: A0 = {indict['A0']} > 2")
    else:
        cc = 0
        print(f"CLEAR PEAK 3 - NO\t: A0 = {indict['A0']} <= 2")
    clear_count.append(cc)
    
    # (4) fpeak[A(f) +/- stdA(f)] = f0 +/- 5%
    F0min = indict['F0'] - (indict['F0'] * 0.05)
    F0max = indict['F0'] + (indict['F0'] * 0.05)
    idminstdhv = argmax(indict['minstdhv'])
    idmaxstdhv = argmax(indict['maxstdhv'])
    if (F0min <= indict['frhv'][idminstdhv] <= F0max and 
        F0min <= indict['frhv'][idmaxstdhv] <= F0max):
        cc = 1
        print(f"CLEAR PEAK 4 - OK\t: fpeak in range [{F0min:.4f}, {F0max:.4f}]")
    else:
        cc = 0
        print(f"CLEAR PEAK 4 - NO\t: fpeak outside range [{F0min:.4f}, {F0max:.4f}]")
    clear_count.append(cc)
    
    # (5) stdF < epsilon(f0)
    if indict['F0'] < 0.2:
        epsf0 = 0.25 * indict['F0']
    elif indict['F0'] < 0.5:
        epsf0 = 0.2 * indict['F0']
    elif indict['F0'] < 1.0:
        epsf0 = 0.15 * indict['F0']
    elif indict['F0'] < 2.0:
        epsf0 = 0.10 * indict['F0']
    else:
        epsf0 = 0.05 * indict['F0']

    if indict['stdf0'] < epsf0:
        cc = 1
        print(f"CLEAR PEAK 5 - OK\t: stdf0 < epsilon(f0) = {indict['stdf0']} < {epsf0}")
    else:
        cc = 0
        print(f"CLEAR PEAK 5 - NO\t: stdf0 >= epsilon(f0) = {indict['stdf0']} >= {epsf0}")
    clear_count.append(cc)
    
    # (6) stdA(f0) < theta(f0)
    if indict['F0'] < 0.2:
        thetaf0 = 0.3
    elif indict['F0'] < 0.5:
        thetaf0 = 2.5
    elif indict['F0'] < 1.0:
        thetaf0 = 2.0
    elif indict['F0'] < 2.0:
        thetaf0 = 1.78
    else:
        thetaf0 = 1.58

    if indict['stdA'] < thetaf0:
        cc = 1
        print(f"CLEAR PEAK 6 - OK\t: stdA(F0) < theta(F0) = {indict['stdA']} < {thetaf0}")
    else:
        cc = 0
        print(f"CLEAR PEAK 6 - NO\t: stdA(F0) >= theta(F0) = {indict['stdA']} >= {thetaf0}")
    clear_count.append(cc)
    
    # Summary
    print("\nCLEAR PEAK SUMMARY\t: %d out of 6 criteria fulfilled" % int(sum(clear_count)))
    if int(sum(clear_count)) >= 5:
        print("CLEAR PEAK SUMMARY\t: H/V IS CLEAR PEAK")
    else:
        print("CLEAR PEAK SUMMARY\t: H/V IS NOT CLEAR PEAK [at least 5 out of 6 criteria fulfilled]")
        print("clear COUNT is :", clear_count)