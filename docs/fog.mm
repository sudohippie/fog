<map version="0.9.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1395954547407" ID="ID_1547388583" MODIFIED="1396471680726" TEXT="fog">
<node CREATED="1395955294785" ID="ID_137285940" MODIFIED="1396464621119" POSITION="left" TEXT="commands">
<node CREATED="1395954807104" ID="ID_1156924238" MODIFIED="1396464657021" TEXT="clone &lt;drive&gt;">
<node CREATED="1395955135745" ID="ID_1474381016" MODIFIED="1395955141574" TEXT="Verifies authentication"/>
<node CREATED="1395955142224" ID="ID_1078412370" MODIFIED="1395955182214" TEXT="recursively pulls src=/ and dst=."/>
</node>
<node CREATED="1395954835792" FOLDED="true" ID="ID_1127056968" MODIFIED="1395955330492" TEXT="rm &lt;remote dst&gt;">
<node CREATED="1395955190832" ID="ID_401066394" MODIFIED="1395955197750" TEXT="Verifies authentication"/>
<node CREATED="1395955198824" ID="ID_1927689269" MODIFIED="1395955225214" TEXT="promts before removing file from src"/>
</node>
<node CREATED="1395954578960" ID="ID_684174885" MODIFIED="1396464642546" TEXT="init">
<node CREATED="1395954895793" ID="ID_1222021449" MODIFIED="1395954905569" TEXT="Need to prive credentials"/>
<node CREATED="1395954906265" ID="ID_614952245" MODIFIED="1395954913920" TEXT="Need to confirm scope"/>
<node CREATED="1395954914496" ID="ID_1549279516" MODIFIED="1395954938566" TEXT="Saves credentials to storage"/>
</node>
<node CREATED="1395954585592" ID="ID_527703676" MODIFIED="1395955862863" TEXT="pull &lt;remote src&gt; [&lt;local dst&gt;]">
<node CREATED="1395954944072" ID="ID_13348305" MODIFIED="1395955007317" TEXT="Verifies authentication"/>
<node CREATED="1395954980328" ID="ID_189017197" MODIFIED="1395955026406" TEXT="registers src and dst"/>
<node CREATED="1395955026856" ID="ID_1283958648" MODIFIED="1395955041741" TEXT="Checks remote for file existence"/>
<node CREATED="1395955118377" ID="ID_1256706401" MODIFIED="1395955125334" TEXT="If file exists at local, prompts"/>
<node CREATED="1395955042265" ID="ID_1918241678" MODIFIED="1395955050006" TEXT="Downloads file from src to dst"/>
</node>
<node CREATED="1395954611912" FOLDED="true" ID="ID_162758302" MODIFIED="1395955333420" TEXT="push &lt;local src&gt; [&lt;remote dst&gt;]">
<node CREATED="1395955053448" ID="ID_1606112464" MODIFIED="1395955058238" TEXT="Verifies authentication"/>
<node CREATED="1395955058536" ID="ID_1613013041" MODIFIED="1395955062726" TEXT="registers src and dst"/>
<node CREATED="1395955063560" ID="ID_203484048" MODIFIED="1395955089286" TEXT="If file exists at remote, prompts"/>
<node CREATED="1395955091649" ID="ID_1718070557" MODIFIED="1395955100422" TEXT="pushes file from src to dst"/>
</node>
<node CREATED="1396464622298" ID="ID_1604315769" MODIFIED="1396464627000" TEXT="checkout &lt;drive&gt;"/>
<node CREATED="1396464630389" ID="ID_171032033" MODIFIED="1396464633430" TEXT="branch"/>
</node>
<node CREATED="1395955349281" ID="ID_859079160" MODIFIED="1395958173237" POSITION="right" TEXT="apis">
<node COLOR="#111111" CREATED="1395955354409" ID="ID_898856602" MODIFIED="1396464983320" TEXT="google python client">
<edge COLOR="#111111" WIDTH="thin"/>
</node>
<node CREATED="1395955362897" ID="ID_708038816" MODIFIED="1395955374456" TEXT="arguments option package"/>
<node CREATED="1395955552985" ID="ID_895986442" MODIFIED="1395955555382" TEXT="logging"/>
</node>
<node CREATED="1395955381241" ID="ID_496929687" MODIFIED="1396470826416" POSITION="right" TEXT=".fog">
<node CREATED="1395955631977" ID="ID_1889088393" MODIFIED="1395958162269" TEXT="googledrive">
<node CREATED="1395955389369" ID="ID_1539642703" MODIFIED="1395955575686" TEXT="configs">
<node CREATED="1395955654145" ID="ID_1665856585" MODIFIED="1395955656743" TEXT="credentials"/>
</node>
</node>
<node CREATED="1396470839058" ID="ID_1569759032" MODIFIED="1396470839775" TEXT="logs">
<node CREATED="1396470865330" ID="ID_119065340" MODIFIED="1396470867144" TEXT="commands"/>
<node CREATED="1396470867994" ID="ID_1674432922" MODIFIED="1396470871263" TEXT="errors"/>
</node>
</node>
<node CREATED="1396464874710" ID="ID_1608634174" MODIFIED="1396464876722" POSITION="left" TEXT="accounts">
<node CREATED="1396464880293" ID="ID_820248433" MODIFIED="1396465288200" TEXT="googledrive">
<node CREATED="1396465294790" ID="ID_1027189188" MODIFIED="1396465299476" TEXT="multiple accounts"/>
</node>
<node CREATED="1396464883022" ID="ID_1665368184" MODIFIED="1396464886212" TEXT="skydrive">
<node CREATED="1396465320190" ID="ID_1597113624" MODIFIED="1396465324092" TEXT="multiple accounts"/>
</node>
<node CREATED="1396464886749" ID="ID_620247651" MODIFIED="1396464893683" TEXT="dropbox">
<node CREATED="1396465326038" ID="ID_1170924201" MODIFIED="1396465329383" TEXT="multiple accounts"/>
</node>
</node>
<node CREATED="1396465561558" ID="ID_1815348815" MODIFIED="1396465564507" POSITION="right" TEXT="authentication">
<node CREATED="1396465565398" ID="ID_1391140335" MODIFIED="1396465577899" TEXT="if not already autheticated, page should be shown"/>
<node CREATED="1396465579230" ID="ID_152627088" MODIFIED="1396465595371" TEXT="after authentication, credentials should be stored"/>
</node>
<node CREATED="1396471682995" ID="ID_1852827748" MODIFIED="1396471760976" POSITION="left" TEXT="operation flow">
<node CREATED="1396472010179" ID="ID_273018072" MODIFIED="1396472014920" TEXT="drive state resolver">
<node CREATED="1396471905714" ID="ID_571144598" MODIFIED="1396471909433" TEXT="drive factory">
<node CREATED="1396471692738" ID="ID_1781772566" MODIFIED="1396471932681" TEXT="executor.execute(command)">
<node CREATED="1396471702418" ID="ID_970207875" MODIFIED="1396471783776" TEXT="authenticator.authenticate()">
<node CREATED="1396471710499" ID="ID_31615652" MODIFIED="1396471795920" TEXT="command.execute()"/>
<node CREATED="1396471845267" ID="ID_1050066924" MODIFIED="1396471848369" TEXT="command needs logging"/>
</node>
<node CREATED="1396471803882" ID="ID_1993260879" MODIFIED="1396471821768" TEXT="authenticator needs config"/>
<node CREATED="1396471822626" ID="ID_764253634" MODIFIED="1396471832400" TEXT="autheticator needs logging"/>
<node CREATED="1396471851114" ID="ID_616260342" MODIFIED="1396471858112" TEXT="logging needs config"/>
</node>
<node CREATED="1396471934364" ID="ID_29156594" MODIFIED="1396471940800" TEXT="executor needs logging"/>
</node>
<node CREATED="1396471942451" ID="ID_1839584741" MODIFIED="1396471947616" TEXT="drive factory needs logging"/>
<node CREATED="1396471948730" ID="ID_1892843975" MODIFIED="1396471957904" TEXT="drive factory needs configuration"/>
</node>
<node CREATED="1396472055531" ID="ID_847533445" MODIFIED="1396472062297" TEXT="drive state resolver needs logging"/>
<node CREATED="1396472063251" ID="ID_1055519443" MODIFIED="1396472068072" TEXT="drive state resolver needs config"/>
</node>
</node>
</map>