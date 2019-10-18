package org.corfudb.elk

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.arguments.argument
import org.apache.commons.compress.archivers.tar.TarArchiveEntry
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream
import org.apache.commons.compress.utils.IOUtils
import org.apache.tools.ant.Project
import org.apache.tools.ant.taskdefs.GUnzip
import java.io.FileInputStream
import java.io.FileOutputStream
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.stream.Collectors


fun main(args: Array<String>) {
    require(args.isNotEmpty()) { "empty parameters" }

    println("Start unpacking! Parameters: ${args.joinToString()}")

    UnpackCmdLine().main(args)
}

class UnpackCmdLine : CliktCommand() {
    companion object {
        val defaultProject: Project = Project()
    }

    private val bug: String by argument(help = "bug")
    private val bundle: String by argument(help = "bundle")

    override fun run() {
        val dataDir = Paths.get("build", "data", bug)
        val destDir = Paths.get("build", "docker-elk", "data", bug)

        dataDir.toFile().mkdirs();

        val unzipped = GzipFile(dataDir, dataDir.resolve(bundle), destDir)
                .unzipBundle()

        val ip = parseIpAddress(destDir, unzipped)

        renameSupportBundleDir(destDir, unzipped, ip)
        val logsDir = Paths.get("build", "docker-elk", "data", bug, ip, "var", "log", "corfu")
        unzipLogs(logsDir)

    }

    fun renameSupportBundleDir(dir: Path, oldName: String, newName: String) {

        //check if already renamed
        val newDir = dir.resolve(newName)
        if (newDir.toFile().exists()) {
            newDir.toFile().deleteRecursively();
        }

        Files.move(dir.resolve(oldName), dir.resolve(newName))
    }

    fun parseIpAddress(dir: Path, bundle: String): String {
        val ifConfig = dir
                .resolve(bundle)
                .resolve("system")
                .resolve("ifconfig_-a")

        return ifConfig.toFile()
                .readLines()[1]
                .trim()
                .split(' ')[1]
                .split(':')[1]
    }

    fun unzipLogs(logsDir: Path) {

        val tgzFiles = Files.list(logsDir)
                .filter { file ->
                    file.toFile().extension == "gz"
                }
                .collect(Collectors.toList())

        tgzFiles.forEach { logFile ->
            println("Unzip: $logFile")
            val unzip = GUnzip()
            unzip.project = defaultProject
            unzip.setSrc(logFile.toFile())
            unzip.execute()

            logFile.toFile().delete()
        }
    }
}

class GzipFile(private val dataDir: Path, private val inputFile: Path, private val outputFile: Path) {

    fun unzipBundle(): String {

        val fis = FileInputStream(inputFile.toFile())
        val gzipIs = GzipCompressorInputStream(fis)

        var name: String? = null;

        TarArchiveInputStream(gzipIs).use { tarIs ->
            var entry: TarArchiveEntry?

            while (true) {
                entry = tarIs.nextTarEntry
                if (entry == null) {
                    break
                }

                if (name == null) {
                    name = entry.name
                }

                if (entry.isDirectory) {
                    continue
                }

                val currFile = outputFile.resolve(entry.name)
                val parent: Path = currFile.parent

                val archive = dataDir.resolve(name!!)
                val varLog = archive.resolve(Paths.get("var", "log", "corfu"))
                val ifConfig = archive.resolve("system").resolve("ifconfig_-a")

                if (dataDir.resolve(entry.name) == ifConfig) {
                    val parentDir = parent.toFile()
                    if (!parentDir.exists()) {
                        parentDir.mkdirs()
                    }

                    IOUtils.copy(tarIs, FileOutputStream(currFile.toFile()))
                }

                if (dataDir.resolve(entry.name).startsWith(varLog)) {
                    val parentDir = parent.toFile()
                    if (!parentDir.exists()) {
                        parentDir.mkdirs()
                    }

                    IOUtils.copy(tarIs, FileOutputStream(currFile.toFile()))
                }
            }
        }

        return name!!
    }
}