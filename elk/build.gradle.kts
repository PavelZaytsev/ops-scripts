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

    val url: String = if (project.hasProperty("url")) project.property("url").toString() else ""
    val bug: String = if (project.hasProperty("bug")) project.property("bug").toString() else ""
    val bundle: String = if (project.hasProperty("bundle")) project.property("bundle").toString() else ""

    commandLine = listOf(
            "sh",
            "-c",
            "java -cp build/libs/elk-corfu.jar org.corfudb.elk.MainKt $bug $bundle $url"
    )
}

task<Exec>("unpack") {
    dependsOn(uberJar)

    workingDir = Paths.get(rootDir.absolutePath).toFile()

    val bug: String = if (project.hasProperty("bug"))
        project.property("bug").toString()
    else ""

    val bundle: String = if (project.hasProperty("bundle"))
        project.property("bundle").toString()
    else ""

    commandLine = listOf(
            "sh",
            "-c",
            "java -cp build/libs/elk-corfu.jar org.corfudb.elk.UnpackKt $bug $bundle"
    )
}

dependencies {
    compile(kotlin("stdlib"))
    implementation("com.github.ajalt:clikt:2.1.0")
    implementation("org.apache.commons:commons-compress:1.19")

    implementation("org.apache.ant:ant:1.10.7")
}

repositories {
    jcenter()
}
