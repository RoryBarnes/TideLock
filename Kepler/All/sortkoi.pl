# SORTKOI.PL
#
# The only Perl script of the repository! This code was originally used in
# Barnes, Meadows and Evans (2015), and I hacked it so that it now runs the
# tidal evolution of the Kepler planets and candidates. It also computes their 
# HITE values. This code relies on both the EQTIDE and HITE codes, which are
# publicly available at https://github.com/RoryBarnes/EqTide and 
# https://github.com/RoryBarnes/HITE. To run:
#
# perl sortkoi.pl
#
$hite="/Users/rory/src/hite/hite";
$eqtide="/Users/rory/src/eqtide/eqtide";

sub LockTime {

    # @_ = name, model, stmass, strad, plmass, plrad, rotper, obl, a

    open TIDE, ">tide.in";
    select TIDE;

    print "# Calculate timescale for circularization\n";
    print "sSystemName           $_[0]\n";
    print "sTideModel            $_[1]\n";
    print "bDiscreteRot          1\n";
    print "\n";
    print "iVerbose              5\n";
    print "iDigits               8\n";
    print "iSciNot               4\n";
    print "\n";
    print "bDoLog                1\n";
    print "\n";
    print "sUnitMass             solar\n";
    print "sUnitLength           AU\n";
    print "sUnitTime             year\n";
    print "sUnitAngle            degrees\n";
    print "\n";
    print "bDoForward            1\n";
    print "bVarDt                1\n";
    print "dForwardStopTime      1.5e10\n";
    print "dForwardOutputTime    1e9\n";
    print "dTimestepCoeff        0.01\n";
    print "dMinValue             1e-10\n";
    print "bHaltSecLock          1\n";
    print "\n";
    print "dPrimaryMass          @_[2]\n";
    print "dPrimaryRadius        -@_[3]\n";
    print "dPrimarySpinPeriod    -30\n";
    print "dPrimaryObliquity     0\n";
    print "dPrimaryRadGyra       0.5\n";
    print "dPrimaryK2            0.5\n";
    print "dPrimaryQ             1e6\n";
    print "dPrimaryTau           -0.01\n";
    print "\n";
    print "dSecondaryMass        -@_[4]\n";
    print "dSecondaryRadius      -@_[5]\n";
    print "dSecondarySpinPeriod  -@_[6]\n";
    print "dSecondaryObliquity   @_[7]\n";
    print "dSecondaryK2          0.3\n";
    print "dSecondaryRadGyra     0.5\n";
    print "dSecondaryQ           @_[8]\n";
    print "dSecondaryTau         -@_[9]\n";
    print "dSecondaryMaxLockDiff 0.1\n";
    print "\n";
    print "dSemi                 @_[10]\n";
    print "dEcc                  0\n";
    print "\n";
    print "sOutputOrder          tim semim ecce -secper -orbperiod secobl\n";

    select STDOUT;
    
    `$eqtide tide.in >& log`;

    open TIDEOUT, "log";
    $tlock=15; # If no halt found, tlock > 15 Gyr
    while (<TIDEOUT>) {
	@words = split " ",$_;
	if ($words[0] eq "HALT:") {
	    if ($words[1] eq "Secondary") {
		$tlock = $words[4]/1e9;
	    }
	}
    }

    return $tlock;
}

$koi="koi_17Aug15.csv";
$plan="plan_18Aug15.csv";
$out="kepler.tlock.dat";
$tex="kepler.tex";

open KOI, "$koi";
open PLAN, "$plan";
open OUT, ">$out";
open TEX, ">$tex";

# First gather all Kepler planets. The NASA Exoplanet Archive does not update
# the KOI table with the properties determined through validation.
for ($j=0;$j<15;$j++) { $foo = <PLAN>; }

$j=0;
while (<PLAN>) {
    $line[$j] = $_;
    @bar=split '\,',$line[$j];
    if (index($bar[1],"Kepler") != -1) { # Kepler planet
	$plan[$j]=$bar[1].$bar[2];
	$planper[$j]=$bar[3];
	$planteff[$j]=$bar[4];
	$planstrad[$j]=$bar[5];
	$planteq[$j]=$bar[6];
	$plandepth[$j]=$bar[7];
	$plandur[$j]=$bar[8];
	$planb[$j]=$bar[9];
	$planlogg[$j]=$bar[10];
	chomp $planlogg[$j];
	$j++;
    }
}

$numplan=$j;

# Now get KOIs
for ($j=0;$j<18;$j++) { $foo = <KOI>; }

$nreplace=0;
$j=0;
while (<KOI>) {
  $line[$j] = $_;
  @bar = split '\,',$line[$j];
  $koi[$j] = $bar[1];
  $kepname[$j] = $bar[2];
  $disp[$j] = $bar[3];
  $per[$j] = $bar[4];
  $b[$j] = $bar[5];
  $dur[$j] = $bar[6];
  $depth[$j] = $bar[7];
  $teq[$j] = $bar[8];
  $teff[$j] = $bar[9];
  $logg[$j] = $bar[10];
  $strad[$j] = $bar[11];
  $kband[$j] = $bar[12];
  $jband[$j] = $bar[13];
  chomp $jband[$j];

  if ($kepname[$j] ne "") {
      # This KOI is a confirmed planet, replace properties with updates
    @bar=split ' ',$kepname[$j];
    $kepname[$j] = $bar[0].$bar[1];
    for ($k=0;$k<$numplan;$k++) {
	if ($kepname[$j] eq $plan[$k]) { # Match
	    print "Replacing $koi[$j] with $plan[$k].\n";
	    $nreplace++;
	    if ($planper[$k] ne "") {
		$per[$j] = $planper[$k];
	    }
	    if ($planb[$k] ne "" && $planb[$k] < 1) {
		$b[$j] = $planb[$k];
	    }
	    if ($plandur[$k] ne "") {
		$dur[$j] = $plandur[$k]*24; # d -> hr
	    }
	    if ($plandepth[$k] ne "") {
		$depth[$j] = $plandepth[$k]*1e4; # % -> ppm
	    }
	    if ($planteq[$k] ne "") {
		$teq[$j] = $planteq[$k];
	    }
	    if ($planteff[$k] ne "") {
		$teff[$j] = $planteff[$k];
	    }
	    if ($planlogg[$k] ne "") {
		$logg[$j] = $planlogg[$k];
	    }
	    if ($planstrad[$k] ne "") {
		$strad[$j] = $planstrad[$k];
	    }
	}
    }
  }
  $j++;
}
$ntot=$j;
print "Replaced $nreplace KOIs.\n";

#die;

#print $line[0];

$nphab=0;
$totphab=0;
for ($j=0;$j<$ntot;$j++) {
  #@bar = split '\,',$line[$j];
  #print $line[$j];
  #print "$bar[0] $bar[8]\n";
  #die;

  if ($teq[$j] ne "" && ($disp[$j] eq "CANDIDATE" || $disp[$j] eq "CONFIRMED")) {
    if ($teq[$j] >= 150 && $teq[$j] <= 400 ) {
    #if ($teq[$j] <= 400 ) {
      #print "$koi[$j] $teq[$j]\n";
      $ok=1;
      if ($koi[$j] eq "") {$ok=0; }
      if ($per[$j] eq "") { $ok=0; }
      if ($b[$j] eq "" || $b[$j] > 1) { $ok=0; }
      if ($dur[$j] eq "") { $ok=0; }
      if ($depth[$j] eq "") { $ok=0; }
      if ($teff[$j] eq "") { $ok=0; }
      if ($strad[$j] eq "") { $ok=0; }
      if ($logg[$j] eq "") { $ok=0; }
      if ($jband[$j] eq "") { $jband[$j] = "20"; }

      if ($ok) {
	# Check for companions
	$ncomp=0;
	@name=split '\.',$koi[$j];
	
	if ($j > 0) {
	  @name0=split '\.',$koi[$j-1];
	  if ($name[0] eq $name0[0]) {
	    #inner planet
	    $iper=$per[$j-1];
	    $ib=$b[$j-1];
	    $idur = $dur[$j-1];
	    $idep = $depth[$j-1];

	    # On what side is the companion?
	    if ($iper < $per[$j]) {
	      $ipos=2;
	    } else {
	      $ipos=3;
	    }

	    $ncomp++;
	  }
	}
      }

      # Only continue tides if isolated planet
      if ($ncomp == 0) {
	# Calculate HITE
	  
	open HITEIN, ">hite.in";
	  
	select HITEIN;
	
	print "NumPlanets\t".($ncomp+1)."\n";
	print "StellarLogG\t$logg[$j]\n";
	print "StellarRadius\t$strad[$j]\n";
	print "StellarTemp\t$teff[$j]\n";
	print "\n";
	
	print "BodyPos\t\t1\n";
	print "TransitDepth\t$depth[$j]\n";
	print "Period\t\t$per[$j]\n";
	print "Duration\t$dur[$j]\n";
	print "ImpactParam\t$b[$j]\n";

	select STDOUT;

	`$hite hite.in`;
	
	open HITEOUT, "hite.out";
	
	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$hprime[$j] = $data[4];

	# print "$j $hprime[$j]\n";
	
	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$h[$j] = $data[4];
	
	for ($k=0;$k<4;$k++) { $baz=<HITEOUT>; }
	
	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$stmass[$j] = $data[3];
	
	for ($k=0;$k<8;$k++) { $baz=<HITEOUT>; }
	
	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$plrad[$j] = $data[2];

	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$plmass[$j] = $data[2];
	
	$baz=<HITEOUT>;
	@data = split ' ',$baz;
	$a[$j] = $data[3];
	
	if ($plrad[$j] < 2.5 && $hprime[$j] > 0.01) {
	  # Phabitable -- calculate tidal evolution
	  if ($kepname[$j] ne "") {
	    $sysname[$j] = $kepname[$j];
	  } else {
	    $sysname[$j] = $koi[$j];
	  }

	  $qpl = 100;
	  $taupl = 64;
	  
	  $rotper=0.33;
	  $obl=60;
	  $model="CPL";

	  $tlockCPLlong[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  $model="CTL";
	  $tlockCTLlong[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  $qpl = 12;
	  $taupl = 640;
	  
	  $rotper=10;
	  $obl=0;
	  $model="CPL";
	  
	  $tlockCPLshort[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  $model="CTL";
	  
	  $tlockCTLshort[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  $qpl=34;
	  $taupl=125;
	  $rotper=1;
	  $obl=23.5;
	  
	  $tlockCTLearth[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  $model="CPL";
	  $tlockCPLearth[$j] = LockTime($sysname[$j],$model,$stmass[$j],$strad[$j],$plmass[$j],$plrad[$j],$rotper,$obl,$qpl,$taupl,$a[$j]);

	  #die;
	  
	  printf OUT "%13s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f ",$sysname[$j],$strad[$j],$stmass[$j],$per[$j],$plrad[$j],$plmass[$j],$a[$j];
	  printf OUT "%.2f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f\n",$hprime[$j],$tlockCPLshort[$j],$tlockCPLearth[$j],$tlockCPLlong[$j],$tlockCTLshort[$j],$tlockCTLearth[$j],$tlockCTLlong[$j];

	  printf TEX "%13s & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f ",$sysname[$j],$strad[$j],$stmass[$j],$per[$j],$plrad[$j],$plmass[$j],$a[$j];
	  printf TEX "%.2f & %6.3f & %6.3f & %6.3f & %6.3f & %6.3f & %6.3f\\\\\n",$hprime[$j],$tlockCPLshort[$j],$tlockCPLearth[$j],$tlockCPLlong[$j],$tlockCTLshort[$j],$tlockCTLearth[$j],$tlockCTLlong[$j];
	}
      }
    }
  }
}

