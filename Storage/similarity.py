'''
This is not used in the app. I am isolating the routine for finding similarity.
'''
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
nltk.download('popular')
import string

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

def tokenize(text):
    '''Create tokenizer and stemmer'''
    tokens = nltk.word_tokenize(text)
    return tokens

def is_ci_token_stopword_set_match(a, b):
    """Check if a and b are matches using Jaccard similarity."""
    tokens_a = [token.lower().strip(string.punctuation) for token in tokenize(a) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenize(b) \
                    if token.lower().strip(string.punctuation) not in stopwords]

    # Jaccard similarity
    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    return ratio

text_a = "## Use Velero to restore a workload cluster You must first create a new cluster to restore to since you cannot restore a cluster backup to an existing cluster. For example, `velero restore create --help` shows all options associated with the `velero restore create` command. If you use Velero to back up multiple clusters with multiple blob containers, it's recommended that you create a unique username per cluster rather than the default name `velero`. You need an active Azure subscription to create an Azure storage account and the blob container as Velero requires both to store backups. On a Windows machine, you can use [Chocolatey](https://chocolatey.org/install) to install the [Velero client](https://chocolatey.org/packages/velero): ```powershell choco install velero ``` 2. If a workload cluster crashes and fails to recover, you can use a Velero backup to restore its contents and internal API objects to a new cluster. By default, Velero stores backups in the same subscription as your VMs and disks and doesn't allow you to restore backups to a resource group in a different subscription."
text_b = "Data written to this volume type persists only for the lifespan of the pod - when the pod is deleted, the volume is deleted. This reclaimPolicy controls the behavior of the underlying storage resource when the pod is deleted and the persistent volume may no longer be required. Multiple pods may need to share the same data volumes or reattach data volumes if the pod is rescheduled on a different node. The storage class also configures the persistent volumes to be expandable, so you just need to edit the persistent volume claim with the new size. ## Persistent volumes Volumes that are defined and created as part of the pod lifecycle only exist until the pod is deleted. The pod definition includes the volume mount once the volume has been connected to the pod. This volume typically uses the underlying local node disk storage, although it can also exist solely in the node's memory."

similar = is_ci_token_stopword_set_match(text_a, text_b)
print(similar)