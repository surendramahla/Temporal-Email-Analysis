name := "Temporal-Email-Analysis"

version := "1.0"

scalaVersion := "2.12.18"

// Spark 3.3.4 dependencies
val sparkVersion = "3.3.4"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core"   % sparkVersion % "provided",
  "org.apache.spark" %% "spark-sql"    % sparkVersion % "provided",
  "org.apache.spark" %% "spark-graphx" % sparkVersion % "provided"
)

// Assembly plugin settings
assembly / assemblyJarName := "temporal-email-analysis.jar"

// Merge strategy for assembly
assembly / assemblyMergeStrategy := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case "reference.conf"              => MergeStrategy.concat
  case x                             => MergeStrategy.first
}

// Fork in run to avoid classpath issues
Compile / run / fork := true

// JVM options for running
javaOptions ++= Seq(
  "-Xmx2g"
)

// Compile target for Java 8
javacOptions ++= Seq("-source", "1.8", "-target", "1.8")

