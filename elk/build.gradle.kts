import java.nio.file.Paths

plugins {
    application
    kotlin("jvm") version "1.3.21"
}

apply {
    from("$rootDir/gradle/idea.gradle.kts")
}

application {
    mainClassName = "org.corfudb.elk.MainKt"
}

val uberJar = tasks.register<Jar>("uberJar") {
    appendix = "corfu"

    from(sourceSets.main.get().output)

    dependsOn(configurations.runtimeClasspath)
    from({
        configurations.runtimeClasspath.get().filter { it.name.endsWith("jar") }.map { zipTree(it) }
    })
}

task<Exec>("processing") {
    dependsOn(uberJar)

    workingDir = Paths.get(rootDir.absolutePath).toFile()

    val url: String = project.property("url").toString()
    val bug: String = project.property("bug").toString()

    commandLine = listOf(
            "sh",
            "-c",
            "java -cp build/libs/elk-corfu.jar org.corfudb.elk.MainKt $bug $url"
    )
}


dependencies {
    compile(kotlin("stdlib"))
    implementation("com.github.ajalt:clikt:2.1.0")
}

repositories {
    jcenter()
}
