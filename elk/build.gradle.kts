plugins {
    application
    kotlin("jvm") version "1.3.21"
}

apply {
    from("$rootDir/gradle/idea.gradle.kts")
}

application {
    mainClassName = "org.corfudb.elk.Main"
}

dependencies {
    compile(kotlin("stdlib"))
}

repositories {
    jcenter()
}
