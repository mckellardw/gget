# Copyright 2022 Laura Luebbert

# Packages for use from terminal
import argparse
import sys
import os
import json

# Custom functions
from .__init__ import __version__
from .gget_ref import ref
from .gget_search import search
from .gget_info import info
from .gget_seq import seq
from .gget_muscle import muscle
from .gget_blast import blast

from .utils import ref_species_options

def main():
    """
    Function containing argparse parsers and arguments to allow the use of gget from the terminal.
    """
    # Define parent parser 
    parent_parser = argparse.ArgumentParser(description=f"gget v{__version__}", add_help=False)
    # Initiate subparsers
    parent_subparsers = parent_parser.add_subparsers(dest="command")
    # Define parent (not sure why I need both parent parser and parent, but otherwise it does not work)
    parent = argparse.ArgumentParser(add_help=False)
    
    # Add custom help argument to parent parser
    parent_parser.add_argument(
            "-h","--help",
            action="store_true",
            help="Print manual. Recommendation: pipe into less by running 'gget -h | less'"
    )
    # Add custom version argument to parent parser
    parent_parser.add_argument(
            "-v","--version",
            action="store_true",
            help="Print version."
    )
    
    ## gget ref subparser
    ref_desc = "Fetch FTPs for reference genomes and annotations by species."
    parser_ref = parent_subparsers.add_parser(
        "ref",
        parents=[parent],
        description=ref_desc,
        help=ref_desc,
        add_help=True
        )
    # ref parser arguments
    parser_ref.add_argument(
        "-s", "--species", 
        default=None,
        type=str,
        help="Species for which the FTPs will be fetched, e.g. homo_sapiens."
    )
    # ref parser arguments
    parser_ref.add_argument(
        "-l", "--list", 
        default=None, 
        action="store_true",
        required=False,
        help="List out all available species."
    )
    parser_ref.add_argument(
        "-w", "--which", 
        default="all", 
        type=str,
        nargs='+',
        required=False,
        help=("Defines which results to return.\n" 
              "Possible entries are:\n"
              "'all' - Returns GTF, cDNA, and DNA links and associated info (default).\n" 
              "Or one or a combination of the following:\n"  
              "'gtf' - Returns the GTF FTP link and associated info.\n" 
              "'cdna' - Returns the cDNA FTP link and associated info.\n"
              "'dna' - Returns the DNA FTP link and associated info."
             )
        )
    parser_ref.add_argument(
        "-r", "--release",
        default=None,  
        type=int, 
        required=False,
        help="Ensemble release the FTPs will be fetched from, e.g. 104 (default: latest Ensembl release).")
    parser_ref.add_argument(
        "-ftp", "--ftp",  
        default=False, 
        action="store_true",
        required=False,
        help="Return only the FTP link instead of a json.")
    parser_ref.add_argument(
        "-d", "--download",  
        default=False, 
        action="store_true",
        required=False,
        help="Download FTPs to the current directory using wget.")
    parser_ref.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "Path to the json file the results will be saved in, e.g. path/to/directory/results.json.\n" 
            "Default: Standard out."
        )
    )

    ## gget search subparser
    parser_gget = parent_subparsers.add_parser(
        "search",
         parents=[parent],
         description="Query Ensembl for genes based on species and free form search terms.", 
         help="Query Ensembl for genes based on species and free form search terms.",
         add_help=True
         )
    # Search parser arguments
    parser_gget.add_argument(
        "-sw", "--searchwords", 
        type=str, 
        nargs="+",
        required=True, 
        help="One or more free form searchwords for the query, e.g. gaba, nmda."
    )
    parser_gget.add_argument(
        "-s", "--species",
        type=str,  
        required=True, 
        help="Species to be queried, e.g. homo_sapiens."
    )
    parser_gget.add_argument(
        "-t", "--seqtype",
        choices=["gene", "transcript"],
        default="gene",
        type=str,  
        required=False, 
        help=(
            "'gene': Returns genes that match the searchwords. (default).\n"
            "'transcript': Returns transcripts that match the searchwords. \n"
        )
    )
    parser_gget.add_argument(
        "-ao", "--andor",
        choices=["and", "or"],
        default="or",
        type=str,  
        required=False, 
        help=(
            "'or': Gene descriptions must include at least one of the searchwords (default).\n"
            "'and': Only return genes whose descriptions include all searchwords.\n"
        )
    )
    parser_gget.add_argument(
        "-l", "--limit",
        type=int, 
        default=None,
        required=False,
        help="Limits the number of results, e.g. 10 (default: None)."
    )
    parser_gget.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "Path to the json file the results will be saved in, e.g. path/to/directory/results.json.\n" 
            "Default: Standard out."
        )
    )
    
    ## gget info subparser
    info_desc = "Fetch gene and transcript metadata using Ensembl IDs."
    parser_info = parent_subparsers.add_parser(
        "info",
        parents=[parent],
        description=info_desc, 
        help=info_desc,
        add_help=True
        )
    # info parser arguments
    parser_info.add_argument(
        "-id", "--ens_ids", 
        type=str,
        nargs="+",
        required=True, 
        help="One or more Ensembl IDs."
    )
    parser_info.add_argument(
        "-e", "--expand", 
        default=False, 
        action="store_true",
        required=False, 
        help=(
            "Expand returned information (only for genes and transcripts) (default: False). "
            "For genes: add isoform information. "
            "For transcripts: add translation and exon information."
        )
    )
    parser_info.add_argument(
        "-H", "--homology", 
        default=False, 
        action="store_true",
        required=False, 
        help="Returns homology information of ID (default: False)."
    )
    parser_info.add_argument(
        "-x", "--xref", 
        default=False, 
        action="store_true",
        required=False, 
        help="Returns information from external references (default: False)."
    )
    parser_info.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "Path to the json file the results will be saved in, e.g. path/to/directory/results.json.\n" 
            "Default: Standard out."
        )
    )
    parser_info.add_argument(
        "-q", "--quiet",
        default=True, 
        action="store_false",
        required=False,
        help="Do not print progress information." 
    )
    
    ## gget seq subparser
    seq_desc = "Fetch nucleotide or amino acid sequence (FASTA) of a gene (and all isoforms) or transcript by Ensembl ID. "
    parser_seq = parent_subparsers.add_parser(
        "seq",
        parents=[parent],
        description=seq_desc, 
        help=seq_desc,
        add_help=True
        )
    # seq parser arguments
    parser_seq.add_argument(
        "-id", "--ens_ids", 
        type=str,
        nargs="+",
        required=True, 
        help="One or more Ensembl IDs."
    )
    parser_seq.add_argument(
        "-st", "--seqtype",
        choices=["gene", "transcript"],
        default="gene",
        type=str,  
        required=False, 
        help=(
            "'gene': Returns nucleotide sequences of the Ensembl IDs (from Ensembl API) (default).\n"
            "'transcript': Returns amino acid sequences of the Ensembl IDs (from UniProt API). \n"
        )
    )
    parser_seq.add_argument(
        "-iso", "--isoforms", 
        default=False, 
        action="store_true",
        required=False, 
        help="Returns sequences of all known transcripts (for gene IDs only) (default: False)."
    )
    parser_seq.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "Path to the FASTA file the results will be saved in, e.g. path/to/directory/results.fa.\n" 
            "Default: Standard out."
        )
    )
    
    ## gget muscle subparser
    muscle_desc = "Align multiple nucleotide or amino acid sequences against each other (using the Muscle v5 algorithm)."
    parser_muscle = parent_subparsers.add_parser(
        "muscle",
        parents=[parent],
        description=muscle_desc, 
        help=muscle_desc,
        add_help=True
        )
    # muscle parser arguments
    parser_muscle.add_argument(
        "-fa", "--fasta", 
        type=str,
        required=True, 
        help="Path to fasta file containing the sequences to be aligned."
    )
    parser_muscle.add_argument(
        "-s5", "--super5", 
        default=False, 
        action="store_true",
        required=False,
        help="If True, align input using Super5 algorithm instead of PPP algorithm to decrease time and memory. Use for large inputs (a few hundred sequences)."
    )
    parser_muscle.add_argument(
        "-o", "--out",
        type=str,
        required=True,
        help="Path to the 'aligned FASTA' (.afa) file the results will be saved in, e.g. path/to/directory/results.afa." 
    )
    
    ## gget blast subparser
    blast_desc = "BLAST a nucleotide or amino acid sequence against any BLAST DB."
    parser_blast = parent_subparsers.add_parser(
        "blast",
        parents=[parent],
        description=blast_desc, 
        help=blast_desc,
        add_help=True
        )
    # blast parser arguments
    parser_blast.add_argument(
        "-s", "--sequence", 
        type=str,
        required=True, 
        help="Sequence (str) or path to fasta file containing one sequence."
    )
    parser_blast.add_argument(
        "-p", "--program", 
        choices=["blastn", "blastp", "blastx", "tblastn", "tblastx"],
        default="default",
        type=str,
        required=False, 
        help=("'blastn', 'blastp', 'blastx', 'tblastn', or 'tblastx'. "
              "Default: 'blastn' for nucleotide sequences; 'blastp' for amino acid sequences.")
    )
    parser_blast.add_argument(
        "-db", "--database", 
        choices=["nt", "nr", "refseq_rna", "refseq_protein", "swissprot", "pdbaa", "pdbnt"],
        default="default",
        type=str,
        required=False, 
        help=("'nt', 'nr', 'refseq_rna', 'refseq_protein', 'swissprot', 'pdbaa', or 'pdbnt'. "
              "Default: 'nt' for nucleotide sequences; 'nr' for amino acid sequences. "
              "More info on BLAST databases: https://ncbi.github.io/blast-cloud/blastdb/available-blastdbs.html")
    )
    parser_blast.add_argument(
        "-ng", "--ncbi_gi", 
        default=False, 
        action="store_true",
        required=False,
        help="Return NCBI GI identifiers. Default False."
    )
    parser_blast.add_argument(
        "-d", "--descriptions", 
        type=int,
        default=500, 
        required=False,
        help="int or None. Limit number of descriptions to return. Default 500."
    )
    parser_blast.add_argument(
        "-a", "--alignments", 
        type=int,
        default=500, 
        required=False,
        help="int or None. Limit number of alignments to return. Default 500."
    )
    parser_blast.add_argument(
        "-hs", "--hitlist_size", 
        type=int,
        default=50, 
        required=False,
        help="int or None. Limit number of hits to return. Default 50."
    )
    parser_blast.add_argument(
        "-e", "--expect", 
        type=float,
        default=10.0, 
        required=False,
        help="float or None. An expect value cutoff. Default 10.0."
    )
    parser_blast.add_argument(
        "-lcf", "--low_comp_filt", 
        default=False, 
        action="store_true",
        required=False,
        help="Turn on low complexity filter. Default off."
    )
    parser_blast.add_argument(
        "-mbo", "--megablast_off", 
        default=True, 
        action="store_false",
        required=False,
        help="Turn off MegaBLAST algorithm. Default on (blastn only)."
    )
    parser_blast.add_argument(
        "-q", "--quiet",
        default=True, 
        action="store_false",
        required=False,
        help="Do not print progress information." 
    )
    parser_blast.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "Path to the csv file the results will be saved in, e.g. path/to/directory/results.csv.\n" 
            "Default: Standard out."
        )
    )
    
    ## Show help when no arguments are given
    if len(sys.argv) == 1:
        parent_parser.print_help(sys.stderr)
        sys.exit(1)

    args = parent_parser.parse_args()

    ### Define return values
    ## Help return
    if args.help:
        # Retrieve all subparsers from the parent parser
        subparsers_actions = [
            action for action in parent_parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            # Get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print("Subparser '{}'".format(choice))
                print(subparser.format_help())
        
    ## Version return
    if args.version:        
        print(f"gget version: {__version__}")

    if args.command == "blast":
        # Run gget blast function
        blast_results = blast(
            sequence = args.sequence,
            program = args.program,
            database = args.database,
            ncbi_gi = args.ncbi_gi,
            descriptions = args.descriptions,
            alignments = args.alignments,
            hitlist_size = args.hitlist_size,
            expect = args.expect,
            low_comp_filt = args.low_comp_filt,
            megablast = args.megablast_off,
            verbose = args.quiet,
            )
        # Save blast results if args.out specified
        if args.out:
            directory = "/".join(args.out.split("/")[:-1])
            if directory != "":
                os.makedirs(directory, exist_ok=True)
            blast_results.to_csv(args.out, index=False)
#             sys.stderr.write(f"\nResults saved as {args.out}.\n")
        
        # Print results if no directory specified
        else:
            blast_results.to_csv(sys.stdout, index=False)
        
    ## muscle return
    if args.command == "muscle":
        muscle(fasta=args.fasta, 
               super5=args.super5,
               out=args.out
              )
        
    ## ref return
    if args.command == "ref":
        # If list flag but no release passed, return all available species for latest release
        if args.list and args.release is None:
                # Find all available species for GTFs for this Ensembl release
                species_list_gtf = ref_species_options('gtf')
                # Find all available species for FASTAs for this Ensembl release
                species_list_dna = ref_species_options('dna') 

                # Find intersection of the two lists 
                # (Only species which have GTF and FASTAs available can continue)
                species_list = list(set(species_list_gtf) & set(species_list_dna))
                
                # Print available species list
                print(species_list)
                
        # If list flag and release passed, return all available species for this release
        if args.list and args.release:
                # Find all available species for GTFs for this Ensembl release
                species_list_gtf = ref_species_options('gtf', release=args.release)
                # Find all available species for FASTAs for this Ensembl release
                species_list_dna = ref_species_options('dna', release=args.release) 

                # Find intersection of the two lists 
                # (Only species which have GTF and FASTAs available can continue)
                species_list = list(set(species_list_gtf) & set(species_list_dna))
                
                # Print available species list
                print(species_list)
        
        # Raise error if neither species nor list flag passed
        if args.species is None and args.list is None:
            parser_ref.error("\n\nThe following arguments are required to fetch FTPs: -s/--species, e.g. '-s homo_sapiens'\n\n"
                             "gget ref --list -> lists out all available species. " 
                             "Combine with [-r] to define specific Ensembl release (default: latest release).")
        
        ## Clean up 'which' entry if passed
        if type(args.which) != str:
            which_clean = []
            # Split by comma (spaces are automatically split by nargs:"+")
            for which in args.which:
                which_clean.append(which.split(","))
            # Flatten which_clean
            which_clean_final = [item for sublist in which_clean for item in sublist]   
            # Remove empty strings resulting from split
            while("" in which_clean_final):
                which_clean_final.remove("")   
        else:
            which_clean_final = args.which

        if args.species:
            
            # Query Ensembl for requested FTPs using function ref
            ref_results = ref(args.species, which_clean_final, args.release, args.ftp)

            # Print or save list of URLs (ftp=True)
            if args.ftp == True:
                # Save in specified directory if -o specified
                if args.out:
                    directory = "/".join(args.out.split("/")[:-1])
                    if directory != "":
                        os.makedirs(directory, exist_ok=True)
                    file = open(args.out, "w")
                    for element in ref_results:
                        file.write(element + "\n")
                    file.close()
#                     sys.stderr.write(
#                         f"\nResults saved as {args.out}.\n"
#                     )
                    
                    if args.download == True:
                        # Download list of URLs
                        for link in ref_results:
                            command = "wget " + link
                            os.system(command)
                    else:
                        sys.stderr.write(
                            "To download the FTPs to the current directory, add flag [-d].\n"
                        )
                
                # Print results if no directory specified
                else:
                    # Print results
                    results = " ".join(ref_results)
                    print(results)
#                     sys.stderr.write("\nTo save these results, use flag '-o' in the format: '-o path/to/directory/results.txt'.\n")
                    
                    if args.download == True:
                        # Download list of URLs
                        for link in ref_results:
                            command = "wget " + link
                            os.system(command)
                    else:
                        sys.stderr.write(
                            "To download the FTPs to the current directory, add flag [-d].\n"
                        )
                    
            # Print or save json file (ftp=False)
            else:
                # Save in specified directory if -o specified
                if args.out:
                    directory = "/".join(args.out.split("/")[:-1])
                    if directory != "":
                        os.makedirs(directory, exist_ok=True)
                    with open(args.out, 'w', encoding='utf-8') as f:
                        json.dump(ref_results, f, ensure_ascii=False, indent=4)
#                     sys.stderr.write(
#                         f"\nResults saved as {args.out}.\n"
#                     )
                    
                    if args.download == True:
                        # Download the URLs from the dictionary
                        for link in ref_results:
                            for sp in ref_results:
                                for ftp_type in ref_results[sp]:
                                    link = ref_results[sp][ftp_type]['ftp']
                                    command = "wget " + link
                                    os.system(command)    
                    else:
                        sys.stderr.write(
                            "To download the FTPs to the current directory, add flag [-d].\n"
                        )
                    
                # Print results if no directory specified
                else:
                    print(json.dumps(ref_results, ensure_ascii=False, indent=4))
#                     sys.stderr.write("\nTo save these results, use flag '-o' in the format: '-o path/to/directory/results.json'.\n")
                    
                    if args.download == True:
                        # Download the URLs from the dictionary
                        for link in ref_results:
                            for sp in ref_results:
                                for ftp_type in ref_results[sp]:
                                    link = ref_results[sp][ftp_type]['ftp']
                                    command = "wget " + link
                                    os.system(command)
                    else:
                        sys.stderr.write(
                            "To download the FTPs to the current directory, add flag [-d].\n"
                        )
        
    ## search return
    if args.command == "search":
        
        ## Clean up args.searchwords
        sw_clean = []
        # Split by comma (spaces are automatically split by nargs:"+")
        for sw in args.searchwords:
            sw_clean.append(sw.split(","))
        # Flatten which_clean
        sw_clean_final = [item for sublist in sw_clean for item in sublist]   
        # Remove empty strings resulting from split
        while("" in sw_clean_final) :
            sw_clean_final.remove("")  
        
        # Query Ensembl for genes based on species and searchwords using function search
        gget_results = search(sw_clean_final, 
                              args.species,
                              seqtype=args.seqtype,
                              andor=args.andor, 
                              limit=args.limit)
        
        # Save in specified directory if -o specified
        if args.out:
            directory = "/".join(args.out.split("/")[:-1])
            if directory != "":
                os.makedirs(directory, exist_ok=True)
            gget_results.to_csv(args.out, index=False)
#             sys.stderr.write(f"\nResults saved as {args.out}.\n")
        
        # Print results if no directory specified
        else:
            gget_results.to_csv(sys.stdout, index=False)
#             sys.stderr.write("\nTo save these results, use flag '-o' in the format: '-o path/to/directory/results.csv'.\n")
            
    ## info return
    if args.command == "info":

        ## Clean up args.ens_ids
        ids_clean = []
        # Split by comma (spaces are automatically split by nargs:"+")
        for id_ in args.ens_ids:
            ids_clean.append(id_.split(","))
        # Flatten which_clean
        ids_clean_final = [item for sublist in ids_clean for item in sublist]   
        # Remove empty strings resulting from split
        while("" in ids_clean_final) :
            ids_clean_final.remove("")  

        # Look up requested Ensembl IDs
        info_results = info(ids_clean_final, expand=args.expand, homology=args.homology, xref=args.xref, verbose=args.quiet)

        # Print or save json file
        # Save in specified directory if -o specified
        if args.out:
            directory = "/".join(args.out.split("/")[:-1])
            if directory != "":
                os.makedirs(directory, exist_ok=True)
            with open(args.out, 'w', encoding='utf-8') as f:
                json.dump(info_results, f, ensure_ascii=False, indent=4)
#             sys.stderr.write(f"\nResults saved as {args.out}.\n")
        # Print results if no directory specified
        else:
            print(json.dumps(info_results, ensure_ascii=False, indent=4))
#             sys.stderr.write("\nTo save these results, use flag '-o' in the format: '-o path/to/directory/results.json'.\n")
            
    ## seq return
    if args.command == "seq":

        ## Clean up args.ens_ids
        ids_clean = []
        # Split by comma (spaces are automatically split by nargs:"+")
        for id_ in args.ens_ids:
            ids_clean.append(id_.split(","))
        # Flatten which_clean
        ids_clean_final = [item for sublist in ids_clean for item in sublist]   
        # Remove empty strings resulting from split
        while("" in ids_clean_final) :
            ids_clean_final.remove("")  

        # Look up requested Ensembl IDs
        seq_results = seq(ids_clean_final, seqtype=args.seqtype, isoforms=args.isoforms)

        # Save in specified directory if -o specified
        if args.out and seq_results != None:
            directory = "/".join(args.out.split("/")[:-1])
            if directory != "":
                os.makedirs(directory, exist_ok=True)
            file = open(args.out, "w")
            for element in seq_results:
                file.write(element + "\n")
            file.close()
#             sys.stderr.write(
#                 f"\nResults saved as {args.out}.\n"
#             )
            
        # Print results if no directory specified
        else:
            if seq_results != None:
                print(seq_results)
#               sys.stderr.write("\nTo save these results, use flag '-o' in the format: '-o path/to/directory/results.fa'.\n")
